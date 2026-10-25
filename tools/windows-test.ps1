# Installs a signed test MSIX from artifacts/windows-test (made by build/windows/build-msix.ps1) in the
# Windows VM, starts it and saves a screenshot of the screen, so a Store package can be tried before upload.
#   prlctl exec "Windows 11" powershell -ExecutionPolicy Bypass -File \\Mac\conc\tools\windows-test.ps1 -Trust
#       (once, as SYSTEM: trusts artifacts/windows-test/test-signing.cer for the whole PC)
#   prlctl exec "Windows 11" --current-user powershell -ExecutionPolicy Bypass -File \\Mac\conc\tools\windows-test.ps1 -Arch arm64
#   ... -Click 640,360       left-click at a screen position, then screenshot (-Wheel -3 scrolls down there instead)
#   ... -Shot name           screenshot only;  -Remove  uninstall
param([string]$Repo = '\\Mac\conc', [string]$Arch, [switch]$Trust, [switch]$Remove, [string]$Click, [int]$Wheel = 0, [string]$Shot = 'screen',
      [string]$Work = 'C:\build\Concentration')
$ErrorActionPreference = 'Stop'
$test = "$Repo\artifacts\windows-test"
$name = '49556nodoid.TheConcntrationGame'

if ($Trust) {
    Import-Certificate -FilePath "$test\test-signing.cer" -CertStoreLocation Cert:\LocalMachine\TrustedPeople | Out-Null
    Write-Host 'test certificate trusted'
    return
}

Add-Type -AssemblyName System.Drawing, System.Windows.Forms
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class Input {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(int f, int x, int y, int d, int e);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, int f, int e);
  public static void Front(IntPtr h) {
    // a background process may only take the foreground after a key event
    keybd_event(0x12, 0, 0, 0); keybd_event(0x12, 0, 2, 0);
    ShowWindow(h, 9); SetForegroundWindow(h);
  }
}
"@
[Input]::SetProcessDPIAware() | Out-Null

function Screenshot($file) {
    $app = Get-Process Concentration -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($app -and $app.MainWindowHandle -ne 0) { [Input]::Front($app.MainWindowHandle); Start-Sleep 1 }
    $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen(0, 0, 0, 0, $bmp.Size)
    New-Item -ItemType Directory -Force "$Repo\artifacts\windows-test\shots" | Out-Null
    $bmp.Save("$Repo\artifacts\windows-test\shots\$file.png", [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    Write-Host "screenshot artifacts\windows-test\shots\$file.png ($($b.Width)x$($b.Height))"
}

if ($Remove) {
    Get-AppxPackage $name | Remove-AppxPackage
    Write-Host 'removed'
    return
}

if ($Arch) {
    Get-Process Concentration -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-AppxPackage $name | Remove-AppxPackage
    # the Windows App SDK runtime the package depends on, as the Store would install it
    $deps = Get-ChildItem "$Work\AppPackages-$Arch" -Recurse -Filter *.msix | Where-Object { $_.DirectoryName -like "*Dependencies\$Arch*" }
    Add-AppxPackage -Path "$test\Concentration-1.0-windows-$Arch.msix" -DependencyPath ($deps.FullName) -ForceUpdateFromAnyVersion
    $pkg = Get-AppxPackage $name
    Write-Host "installed $($pkg.PackageFullName)"
    Start-Process "shell:AppsFolder\$($pkg.PackageFamilyName)!App"
    Start-Sleep 12
    $p = Get-Process Concentration -ErrorAction SilentlyContinue
    if (-not $p) { throw 'Concentration is not running' }
    Write-Host "running: pid $($p.Id), $([Math]::Round($p.WorkingSet64 / 1MB)) MB, main window '$($p.MainWindowTitle)'"
    Screenshot "$Arch-$Shot"
    return
}

if ($Click) {
    $app = Get-Process Concentration -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($app) { [Input]::Front($app.MainWindowHandle); Start-Sleep 1 }
    $x, $y = $Click.Split(',') | ForEach-Object { [int]$_ }
    [Input]::SetCursorPos($x, $y) | Out-Null
    if ($Wheel) { [Input]::mouse_event(0x800, 0, 0, 120 * $Wheel, 0) }
    else { [Input]::mouse_event(2, 0, 0, 0, 0); Start-Sleep -Milliseconds 80; [Input]::mouse_event(4, 0, 0, 0, 0) }
    Start-Sleep 2
}
if (-not (Get-Process Concentration -ErrorAction SilentlyContinue)) { throw 'Concentration is not running' }
Screenshot $Shot
