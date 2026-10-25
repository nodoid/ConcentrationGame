#!/usr/bin/env bash
# Captures Mac App Store screenshots with the screenshot driver (the window opens at 1440x900).
#
#   dotnet build Concentration/Concentration.csproj -f net10.0-maccatalyst -c Debug -p:Screenshots=true -o artifacts/shots-mac
#   swiftc -O tools/winid.swift -o artifacts/winid
#   tools/capture-mac.sh <output dir>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTDIR="$1"
APP="$ROOT/artifacts/shots-mac/Concentration.app"
# unsandboxed (screenshot build), the app's data directory is ~/Library
DB="$HOME/Library/concscore.db3"
mkdir -p "$OUTDIR"

shoot() { # $1 = shot, $2 = seconds to let it play out, $3 = file name
  pkill -f "$APP/Contents/MacOS/Concentration" 2>/dev/null || true
  sleep 1
  # start each shot with an empty high score table, as on a fresh install
  rm -f "$DB" "$DB-journal" "$DB-wal" "$DB-shm"
  CONC_SHOT="$1" "$APP/Contents/MacOS/Concentration" >/dev/null 2>&1 &
  sleep "$2"
  local id
  id="$("$ROOT/artifacts/winid" Concentration)"
  screencapture -o -x -l "$id" "$OUTDIR/$3"
  echo "  $3"
}

shoot title 8 01-title.png
shoot play 14 02-play.png
shoot board 14 03-board.png
shoot win 16 04-win.png
shoot scores 20 05-scores.png
pkill -f "$APP/Contents/MacOS/Concentration" 2>/dev/null || true
