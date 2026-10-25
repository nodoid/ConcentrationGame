# Store assets

Everything here except `copy/` and this README is generated and git-ignored. The screenshots come from the real app, driven by `Concentration/Helpers/ScreenshotDriver.cs` (compiled only with `-p:Screenshots=true`, never in store builds), so every frame is genuine play:

```bash
# iOS (iPhone 17 Pro Max, iPhone 17 Pro, iPad Pro 13" simulators)
dotnet build Concentration/Concentration.csproj -f net10.0-ios -c Debug -r iossimulator-arm64 -p:Screenshots=true -o artifacts/shots-ios
tools/capture-ios.sh <udid> artifacts/capture/iphone-6.9   # also iphone-6.3, ipad-13

# Mac (unsandboxed: an ad-hoc signed app cannot start inside the App Sandbox)
dotnet build Concentration/Concentration.csproj -f net10.0-maccatalyst -c Debug -p:Screenshots=true \
  -p:CodesignEntitlements=$PWD/artifacts/no-entitlements.plist -o artifacts/shots-mac
swiftc -O tools/winid.swift -o artifacts/winid
tools/capture-mac.sh artifacts/capture/mac

# Android (running arm64 emulator with ~400 MB free)
dotnet build Concentration/Concentration.csproj -f net10.0-android -c Release -r android-arm64 -p:Screenshots=true \
  -p:AndroidPackageFormats=apk -o artifacts/shots-android
tools/capture-android.sh 1080x2160 420 artifacts/capture/android-phone
tools/capture-android.sh 1200x1920 240 artifacts/capture/android-tablet-7
tools/capture-android.sh 1600x2560 320 artifacts/capture/android-tablet-10

# Windows, in the Parallels VM (repo shared as \\Mac\conc; build/windows/build-msix.ps1 copies the source in first)
prlctl exec "Windows 11" --current-user powershell -ExecutionPolicy Bypass -File '\\Mac\conc\tools\capture-windows.ps1'

python3 tools/store_assets.py   # screenshots at exact store sizes, Play icon, feature graphic, Microsoft Store art
python3 tools/store_copy.py     # copy/en/*.txt
python3 tools/support_page.py   # ~/Downloads/Concentration-Support.html (support + privacy policy)

# iPad app preview: a whole Medium game, with the game's sounds mixed in -> ~/Movies
python3 tools/record_ipad_preview.py <iPad Pro 13-inch udid>   # after the iOS build above
```

| Folder | Contents |
|---|---|
| `ios/iphone-6.9in` (1320x2868, **required**), `ios/iphone-6.3in` (1206x2622), `ios/ipad-13in` (2064x2752, **required**) | 5 screenshots each |
| `macos/` (1440x900) | 5 screenshots |
| `android/phone` (1080x2160), `tablet-7in` (1200x1920), `tablet-10in` (1600x2560), `feature-graphic-1024x500.png`, `icon-512.png` | Google Play |
| `windows/` (1920x1080) + `windows/art/` (tile icon, box, poster and super hero art) + `windows/xbox/` (Xbox key art, titled hero art, promotional square) | Microsoft Store |
| `copy/en/ios.txt`, `macos.txt`, `android.txt`, `windows.txt` | Every field each store form asks for, with character counts |
| `~/Movies/Concentration - iPad app preview 1200x1600 - English.mp4` | 29 s App Store app preview: H.264 10 Mbps 30 fps, AAC stereo |
| `~/Downloads/Concentration-Support.html` | Support page with the privacy policy at `#privacy`; one self-contained file |

The shots are: 01 title, 02 an Easy game in progress, 03 a Medium game, 04 a cleared Hard game, 05 the high score table.

Packages are built by `build/build-release.sh` into `releases/`. The Windows MSIX files (x64 and arm64) are built in the Parallels VM and left unsigned for Partner Center; `tools/windows-test.ps1` installs the signed test copies from `artifacts/windows-test` to try them first.
