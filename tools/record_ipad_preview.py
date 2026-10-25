#!/usr/bin/env python3
"""Records the iPad App Store app preview: a whole Medium game played by the screenshot driver.

    dotnet build Concentration/Concentration.csproj -f net10.0-ios -c Debug -r iossimulator-arm64 \\
      -p:Screenshots=true -o artifacts/shots-ios
    python3 tools/record_ipad_preview.py <iPad Pro 13-inch simulator udid>
    python3 tools/record_ipad_preview.py --encode   # re-encode the last recording only

The simulator records no audio, so the driver logs the time of every sound the game plays and the
game's own .wav files are mixed in at those times. Output: ~/Movies, 1200x1600 H.264 30 fps with
stereo AAC, 15-30 seconds (the App Store app preview spec for 13-inch iPad).
"""
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "artifacts" / "shots-ios" / "Concentration.app"
BUNDLE = "uk.co.all-the-johnsons.concentration"
RAW = ROOT / "Concentration" / "Resources" / "Raw"
WORK = ROOT / "artifacts" / "preview"
OUT = Path.home() / "Movies" / "Concentration - iPad app preview 1200x1600 - English.mp4"
HOLD = 3.5      # seconds the high score table stays on screen
LEAD_IN = 0.3   # seconds after the title screen appears


def sim(*args, **kw):
    return subprocess.run(["xcrun", "simctl", *args], check=True, capture_output=True, text=True, **kw).stdout


def record(udid):
    WORK.mkdir(parents=True, exist_ok=True)
    mov = WORK / "ipad.mov"
    subprocess.run(["xcrun", "simctl", "boot", udid], capture_output=True)
    sim("bootstatus", udid, "-b")
    sim("status_bar", udid, "override", "--time", "9:41", "--dataNetwork", "wifi", "--wifiMode", "active",
        "--wifiBars", "3", "--batteryState", "charged", "--batteryLevel", "100")
    sim("ui", udid, "appearance", "light")
    subprocess.run(["xcrun", "simctl", "uninstall", udid, BUNDLE], capture_output=True)
    sim("install", udid, str(APP))

    rec = subprocess.Popen(["xcrun", "simctl", "io", udid, "recordVideo", "--codec=h264", "--force", str(mov)],
                           stderr=subprocess.PIPE, text=True)
    started = threading.Event()
    start_ms = [0]

    def watch():
        for line in rec.stderr:
            if "Recording started" in line and not started.is_set():
                start_ms[0] = int(time.time() * 1000)
                started.set()

    threading.Thread(target=watch, daemon=True).start()
    if not started.wait(20):
        sys.exit("recordVideo did not start")

    sim("launch", udid, BUNDLE, env={**os.environ, "SIMCTL_CHILD_CONC_SHOT": "demo"})
    deadline = time.time() + 90
    while time.time() < deadline:
        log = find_log(udid)
        if log and "scores" in log.read_text():
            break
        time.sleep(0.5)
    else:
        rec.send_signal(signal.SIGINT)
        sys.exit("the demo did not reach the high score table")
    time.sleep(HOLD + 1)
    rec.send_signal(signal.SIGINT)
    rec.wait(30)
    subprocess.run(["xcrun", "simctl", "terminate", udid, BUNDLE], capture_output=True)

    events = []
    for line in log.read_text().split("\n"):
        if line.strip():
            ms, evt = line.split(" ", 1)
            events.append(((int(ms) - start_ms[0]) / 1000, evt))
    (WORK / "events.txt").write_text("".join(f"{t:.3f} {e}\n" for t, e in events))
    return mov, events


def find_log(udid):
    # AppDataDirectory is Library on iOS; fall back to a search if that ever changes
    data = Path(sim("get_app_container", udid, BUNDLE, "data").strip())
    hits = list(data.rglob("demo-events.txt"))
    return hits[0] if hits else None


def encode(mov, events):
    t0 = next(t for t, e in events if e == "title") + LEAD_IN
    end = next(t for t, e in events if e == "scores") + HOLD
    length = min(end - t0, 30.0)
    if length < 15:
        sys.exit(f"preview is only {length:.1f}s; the App Store needs 15-30s")

    sounds = [(t - t0, e.split()[1]) for t, e in events if e.startswith("sound ") and t0 <= t < t0 + length]
    inputs = ["-i", str(mov)]
    # the simulator writes a frame only when the screen changes: make it 30 fps (repeating frames,
    # holding the last to the end) before cutting, or a cut between frames loses the picture on screen
    graph = [f"[0:v]tpad=stop_mode=clone:stop_duration=10,fps=30,trim=start={t0:.3f}:duration={length:.3f},"
             f"setpts=PTS-STARTPTS,scale=1200:1600:flags=lanczos,format=yuv420p,setsar=1[v]"]
    mix = []
    for i, (t, name) in enumerate(sounds, start=1):
        inputs += ["-i", str(RAW / f"{name}.wav")]
        ms = max(0, round(t * 1000))
        graph.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]")
        mix.append(f"[a{i}]")
    # a silent bed makes the track exactly as long as the video
    inputs += ["-f", "lavfi", "-t", f"{length:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    mix.append(f"[{len(sounds) + 1}:a]")
    graph.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=longest:normalize=0,"
                 f"alimiter=limit=0.9,atrim=0:{length:.3f}[a]")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(graph),
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-profile:v", "high", "-level", "4.0", "-preset", "slow",
                    # the App Store asks for 10-12 Mbps; filler keeps the mostly still picture at 10
                    "-b:v", "10M", "-minrate", "10M", "-maxrate", "10M", "-bufsize", "10M",
                    "-x264-params", "nal-hrd=cbr:filler=1", "-r", "30",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", "-t", f"{length:.3f}", str(OUT)], check=True)
    print(f"{OUT}: {length:.1f}s, {len(sounds)} sounds")


if __name__ == "__main__":
    if sys.argv[1] == "--encode":
        saved = [line.split(" ", 1) for line in (WORK / "events.txt").read_text().splitlines()]
        encode(WORK / "ipad.mov", [(float(t), e) for t, e in saved])
    else:
        encode(*record(sys.argv[1]))
