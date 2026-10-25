# Captures Microsoft Store screenshots (1920x1080) with the screenshot driver, inside the Windows VM.
# From the Mac, with the repo shared into Parallels as \\Mac\conc (build/windows/build-msix.ps1 copies the source):
#   prlctl exec "Windows 11" --current-user powershell -ExecutionPolicy Bypass -File \\Mac\conc\tools\capture-windows.ps1
# While capturing, the screen is set to 2560x1600 at 100% scaling so the 1920x1080 page fits in real pixels;
# the resolution and scaling are put back afterwards.
param([string]$Repo = '\\Mac\conc', [string]$Work = 'C:\build\Concentration', [string]$OutDir = '\\Mac\conc\artifacts\capture\windows')
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class Win {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr v);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, int f, int e);
  [DllImport("user32.dll")] public static extern bool SystemParametersInfo(int a, int p, IntPtr v, int f);
  [DllImport("user32.dll")] public static extern IntPtr MonitorFromPoint(long pt, int f);
  [DllImport("shcore.dll")] public static extern int GetDpiForMonitor(IntPtr m, int t, out uint x, out uint y);
  public static uint Dpi() { uint x, y; GetDpiForMonitor(MonitorFromPoint(0, 1), 0, out x, out y); return x; }
  // scaling relative to Windows' recommendation for the screen: 0 = recommended, -1 = one step smaller...
  public static void ScaleStep(int relative) { SystemParametersInfo(0x9F, relative, IntPtr.Zero, 1); }
  // a background process may only take the foreground after a key event
  public static void Front(IntPtr h) { keybd_event(0x12, 0, 0, 0); keybd_event(0x12, 0, 2, 0); SetForegroundWindow(h); }

  [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)]
  public struct DEVMODE {
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst=32)] public string dmDeviceName;
    public short dmSpecVersion, dmDriverVersion, dmSize, dmDriverExtra; public int dmFields;
    public int dmPositionX, dmPositionY, dmDisplayOrientation, dmDisplayFixedOutput;
    public short dmColor, dmDuplex, dmYResolution, dmTTOption, dmCollate;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst=32)] public string dmFormName;
    public short dmLogPixels; public int dmBitsPerPel, dmPelsWidth, dmPelsHeight, dmDisplayFlags, dmDisplayFrequency;
    public int dmICMMethod, dmICMIntent, dmMediaType, dmDitherType, dmReserved1, dmReserved2, dmPanningWidth, dmPanningHeight;
  }
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern bool EnumDisplaySettingsW(string d, int m, ref DEVMODE dm);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int ChangeDisplaySettingsW(ref DEVMODE dm, int f);
  public static int[] Size() { var dm = new DEVMODE(); dm.dmSize = (short)Marshal.SizeOf(typeof(DEVMODE)); EnumDisplaySettingsW(null, -1, ref dm); return new[] { dm.dmPelsWidth, dm.dmPelsHeight }; }
  public static int SetSize(int w, int h) {
    var dm = new DEVMODE(); dm.dmSize = (short)Marshal.SizeOf(typeof(DEVMODE)); EnumDisplaySettingsW(null, -1, ref dm);
    dm.dmPelsWidth = w; dm.dmPelsHeight = h; dm.dmFields = 0x80000 | 0x100000; return ChangeDisplaySettingsW(ref dm, 0);
  }
}
"@
[Win]::SetProcessDpiAwarenessContext([IntPtr]-4) | Out-Null  # per-monitor aware: real pixels

$shots = "$Work\shots"
dotnet build "$Work\Concentration\Concentration.csproj" -f net10.0-windows10.0.26100.0 -p:TargetFrameworks=net10.0-windows10.0.26100.0 -c Release -r win-arm64 `
    -p:Screenshots=true -p:WindowsPackageType=None -p:WindowsAppSDKSelfContained=true -p:SelfContained=true `
    -o $shots -nologo -v:minimal
if ($LASTEXITCODE) { throw 'screenshot build failed' }
$exe = "$shots\Concentration.exe"

$old = [Win]::Size()
if ([Win]::SetSize(2560, 1600)) { throw 'could not set the screen to 2560x1600' }
Start-Sleep 2
$step = 0
while ([Win]::Dpi() -gt 96 -and $step -gt -8) { $step--; [Win]::ScaleStep($step); Start-Sleep 2 }
if ([Win]::Dpi() -ne 96) { throw "could not set 100% scaling (dpi $([Win]::Dpi()))" }
New-Item -ItemType Directory -Force $OutDir | Out-Null

function Shoot($shot, $seconds, $file) {
    Get-Process Concentration -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep 1
    # start each shot with an empty high score table, as on a fresh install
    Get-ChildItem $env:LOCALAPPDATA -Recurse -Depth 4 -Filter 'concscore.db3*' -ErrorAction SilentlyContinue | Remove-Item -Force
    $env:CONC_SHOT = $shot
    $p = Start-Process $exe -PassThru
    Start-Sleep $seconds
    $p.Refresh()
    $h = $p.MainWindowHandle
    [Win]::Front($h)
    Start-Sleep 1
    $r = New-Object Win+RECT; [Win]::GetClientRect($h, [ref]$r) | Out-Null
    $o = New-Object Win+POINT; [Win]::ClientToScreen($h, [ref]$o) | Out-Null
    # the bottom 1080 pixels of the client area: the page, without the title bar MAUI draws in it
    $w = $r.Right; $ht = [Math]::Min($r.Bottom, 1080)
    $bmp = New-Object System.Drawing.Bitmap $w, $ht
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($o.X, $o.Y + $r.Bottom - $ht, 0, 0, $bmp.Size)
    $bmp.Save("$OutDir\$file", [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    Write-Host "  $file ($w x $ht, client $($r.Right) x $($r.Bottom))"
}

try {
    Shoot title 10 01-title.png
    Shoot play 16 02-play.png
    Shoot board 16 03-board.png
    Shoot win 18 04-win.png
    Shoot scores 22 05-scores.png
}
finally {
    Get-Process Concentration -ErrorAction SilentlyContinue | Stop-Process -Force
    [Win]::ScaleStep(0)
    [Win]::SetSize($old[0], $old[1]) | Out-Null
}
