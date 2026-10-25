#!/usr/bin/env bash
# Builds signed store packages into releases/.
#
#   build/build-release.sh [all|android|ios|macos|windows]
#
# Needs (macOS host): .NET 10 SDK with maui/android/ios/maccatalyst workloads, Xcode, the
# conc-rel-ios / conc-rel-mac App Store provisioning profiles, the Apple Distribution and
# 3rd Party Mac Developer Installer identities in the keychain, signing/local.properties
# (see build/local.properties.example) and signing/android.properties (Play upload key).
# Windows (WinUI does not build on macOS) is built in the Parallels VM "Windows 11" by
# build/windows/build-msix.ps1, with this repo shared into it as \\Mac\conc:
#   prlctl set "Windows 11" --shf-host-add conc --path "$PWD" --mode rw
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PROJ="Concentration/Concentration.csproj"
VERSION=$(sed -n 's:.*<ApplicationDisplayVersion>\(.*\)</ApplicationDisplayVersion>.*:\1:p' "$PROJ")
BUILD=$(sed -n 's:.*<ApplicationVersion>\(.*\)</ApplicationVersion>.*:\1:p' "$PROJ")
NAME="Concentration"
OUT="$ROOT/releases"
WORK="$ROOT/artifacts/work"
TARGET="${1:-all}"

LOCAL="$ROOT/signing/local.properties"
[ -f "$LOCAL" ] || { echo "Missing $LOCAL - copy build/local.properties.example"; exit 1; }
# shellcheck disable=SC1090
source "$LOCAL"

# Always build releases from clean.
rm -rf "$WORK" Concentration/bin/Release Concentration/obj/Release
mkdir -p "$OUT" "$WORK"
echo "$NAME $VERSION ($BUILD) -> $OUT"

build_android() {
  echo "== Android"
  local props="$ROOT/signing/android.properties"
  [ -f "$props" ] || { echo "Missing $props (Play upload key)"; exit 1; }
  # shellcheck disable=SC1090
  source "$props"
  dotnet publish "$PROJ" -f net10.0-android -c Release -o "$WORK/android" \
    -p:AndroidPackageFormats="aab%3Bapk" \
    -p:AndroidKeyStore=true \
    -p:AndroidSigningKeyStore="$ROOT/signing/$KEYSTORE_FILE" \
    -p:AndroidSigningKeyAlias="$KEY_ALIAS" \
    -p:AndroidSigningStorePass="env:CONCENTRATION_STORE_PASS" \
    -p:AndroidSigningKeyPass="env:CONCENTRATION_STORE_PASS"
  # publish copies only the .aab; the signed .apk stays in bin/
  cp "$(find "$WORK/android" -name '*-Signed.aab' | head -1)" "$OUT/$NAME-$VERSION-android.aab"
  cp "$(find Concentration/bin/Release/net10.0-android -name '*-Signed.apk' | head -1)" "$OUT/$NAME-$VERSION-android.apk"
}

build_ios() {
  echo "== iOS (App Store)"
  dotnet publish "$PROJ" -f net10.0-ios -c Release -r ios-arm64 -o "$WORK/ios" \
    -p:ArchiveOnBuild=false -p:BuildIpa=true -p:ProvisioningType=manual \
    -p:CodesignKey="$APPLE_DIST_IDENTITY" -p:CodesignProvision="$IOS_PROFILE_NAME"
  cp "$(find "$WORK/ios" -name '*.ipa' | head -1)" "$OUT/$NAME-$VERSION-ios.ipa"
}

build_macos() {
  echo "== macOS (Mac App Store, x64 + arm64)"
  dotnet publish "$PROJ" -f net10.0-maccatalyst -c Release -o "$WORK/macos" \
    -p:CreatePackage=false -p:EnableCodeSigning=true \
    -p:CodesignKey="$APPLE_DIST_IDENTITY" -p:CodesignProvision="$MAC_PROFILE_NAME" \
    -p:CodesignEntitlements=Platforms/MacCatalyst/Entitlements.plist
  local app pkg="$OUT/$NAME-$VERSION-macos.pkg"
  app="Concentration/bin/Release/net10.0-maccatalyst/$NAME.app"  # the universal (x64 + arm64) bundle
  # NuGet's files carry com.apple.provenance, which would be packed into the .pkg payload and
  # App Store Connect rejects any extended attribute (error 91109). They are not part of the signature.
  xattr -cr "$app"
  codesign --verify --deep --strict "$app"
  productbuild --component "$app" /Applications --sign "$MAC_INSTALLER_IDENTITY" "$pkg"
  check_pkg_xattrs "$pkg"
  pkgutil --check-signature "$pkg" | head -3
}

check_pkg_xattrs() {
  local tmp found
  tmp="$(mktemp -d)"
  (cd "$tmp" && xar -xf "$1" && mkdir x && cd x && gunzip -dc "$(find .. -name Payload -type f | head -1)" | cpio -i --quiet)
  found="$(xattr -lr "$tmp/x" 2>/dev/null; find "$tmp/x" -name '._*')"
  rm -rf "$tmp"
  [ -z "$found" ] || { echo "ERROR: $1 payload carries extended attributes:"; echo "$found" | head; exit 1; }
  echo "No extended attributes in $(basename "$1") payload"
}

build_windows() {
  # MSIX for x64 and arm64 (unsigned: Partner Center signs them), plus signed test copies in artifacts/windows-test
  echo "== Windows (MSIX: x64 + arm64, in Parallels)"
  prlctl exec "${WINDOWS_VM:-Windows 11}" --current-user powershell -NoProfile -ExecutionPolicy Bypass \
    -File '\\Mac\conc\build\windows\build-msix.ps1'
}

case "$TARGET" in
  android) build_android ;;
  ios) build_ios ;;
  macos) build_macos ;;
  windows) build_windows ;;
  all) build_android; build_ios; build_macos; build_windows ;;
  *) echo "unknown target $TARGET"; exit 1 ;;
esac

rm -rf "$WORK"
echo "Done:"; ls -lh "$OUT"
