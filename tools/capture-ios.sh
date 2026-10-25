#!/usr/bin/env bash
# Captures App Store screenshots from the iOS simulator with the screenshot driver.
#
#   dotnet build Concentration/Concentration.csproj -f net10.0-ios -c Debug -r iossimulator-arm64 \
#     -p:Screenshots=true -o artifacts/shots-ios
#   tools/capture-ios.sh <simulator udid> <output dir>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UDID="$1"
OUTDIR="$2"
APP="$ROOT/artifacts/shots-ios/Concentration.app"
BUNDLE="uk.co.all-the-johnsons.concentration"
mkdir -p "$OUTDIR"

xcrun simctl boot "$UDID" 2>/dev/null || true
xcrun simctl bootstatus "$UDID" -b >/dev/null
xcrun simctl status_bar "$UDID" override --time 9:41 --dataNetwork wifi --wifiMode active --wifiBars 3 \
  --cellularMode active --cellularBars 4 --batteryState charged --batteryLevel 100
xcrun simctl ui "$UDID" appearance light

shoot() { # $1 = shot, $2 = seconds to let it play out, $3 = file name
  xcrun simctl uninstall "$UDID" "$BUNDLE" 2>/dev/null || true
  xcrun simctl install "$UDID" "$APP"
  SIMCTL_CHILD_CONC_SHOT="$1" xcrun simctl launch "$UDID" "$BUNDLE" >/dev/null
  sleep "$2"
  xcrun simctl io "$UDID" screenshot --type=png "$OUTDIR/$3" >/dev/null 2>&1
  echo "  $3"
}

shoot title 8 01-title.png
shoot play 14 02-play.png
shoot board 14 03-board.png
shoot win 16 04-win.png
shoot scores 20 05-scores.png
xcrun simctl terminate "$UDID" "$BUNDLE" 2>/dev/null || true
