#!/usr/bin/env bash
# Captures Google Play screenshots on a running emulator with the screenshot driver.
#
#   dotnet build Concentration/Concentration.csproj -f net10.0-android -c Debug -p:Screenshots=true \
#     -p:EmbedAssembliesIntoApk=true -p:AndroidPackageFormats=apk -o artifacts/shots-android
#   tools/capture-android.sh <width>x<height> <density> <output dir>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$HOME/Library/Android/sdk/platform-tools:$PATH"
SIZE="$1"
DENSITY="$2"
OUTDIR="$3"
APK="$ROOT/artifacts/shots-android/uk.co.allthejohnsons.concentration-Signed.apk"
PKG="uk.co.allthejohnsons.concentration"
mkdir -p "$OUTDIR"

adb shell wm size "$SIZE"
adb shell wm density "$DENSITY"
# clean status bar: 09:41, full battery and signal, no notifications
adb shell settings put global sysui_demo_allowed 1
demo() { adb shell am broadcast -a com.android.systemui.demo -e command "$@" >/dev/null; }
demo enter
demo clock -e hhmm 0941
demo battery -e level 100 -e plugged false
demo network -e wifi show -e level 4 -e mobile show -e datatype none -e level 4
demo notifications -e visible false

shoot() { # $1 = shot, $2 = seconds to let it play out, $3 = file name
  adb uninstall "$PKG" >/dev/null 2>&1 || true
  adb install -r "$APK" >/dev/null
  adb shell am start -n "$(adb shell cmd package resolve-activity --brief "$PKG" | tail -1 | tr -d '\r')" -e shot "$1" >/dev/null
  sleep "$2"
  adb exec-out screencap -p > "$OUTDIR/$3"
  echo "  $3"
}

shoot title 10 01-title.png
shoot play 16 02-play.png
shoot board 16 03-board.png
shoot win 18 04-win.png
shoot scores 22 05-scores.png

adb shell am force-stop "$PKG"
demo exit
adb shell wm size reset
adb shell wm density reset
