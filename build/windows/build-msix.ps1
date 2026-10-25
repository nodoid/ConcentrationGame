# Builds the Microsoft Store packages (MSIX, x64 and arm64) on Windows. MAUI's WinUI target only builds there.
# From the Mac, with the repo shared into the Parallels VM as \\Mac\conc:
#   prlctl exec "Windows 11" --current-user powershell -ExecutionPolicy Bypass -File \\Mac\conc\build\windows\build-msix.ps1
#
# releases/Concentration-<version>-windows-<arch>.msix  unsigned; Partner Center signs Store packages
# artifacts/windows-test/*.msix                         signed with a local test certificate for sideloading
param([string]$Repo = '\\Mac\conc', [string]$Work = 'C:\build\Concentration', [string[]]$Archs = @('x64', 'arm64'))
$ErrorActionPreference = 'Stop'

robocopy "$Repo\Concentration" "$Work\Concentration" /MIR /XD bin obj /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed ($LASTEXITCODE)" }

[xml]$proj = Get-Content "$Work\Concentration\Concentration.csproj"
$version = @($proj.Project.PropertyGroup.ApplicationDisplayVersion | Where-Object { $_ })[0]
$tfm = 'net10.0-windows10.0.26100.0'
New-Item -ItemType Directory -Force "$Repo\releases", "$Repo\artifacts\windows-test" | Out-Null

foreach ($arch in $Archs) {
    Write-Host "== Windows $arch"
    $out = "$Work\AppPackages-$arch"
    Remove-Item -Recurse -Force $out -ErrorAction SilentlyContinue
    # self-contained: Store customers needn't have the .NET Desktop Runtime installed (the Windows App SDK
    # runtime is a package dependency the Store installs itself); TargetFrameworks is narrowed so restoring with a Windows RID leaves the mobile targets alone;
    # the Store keeps the fourth part of the package version for itself, so it must be 0:
    # ApplicationDisplayVersion 1.0 with ApplicationVersion 0 gives 1.0.0.0 (raise the display version for updates)
    dotnet publish "$Work\Concentration\Concentration.csproj" -f $tfm -p:TargetFrameworks=$tfm -c Release -r win-$arch -p:Platform=$arch `
        -p:ApplicationVersion=0 -p:SelfContained=true -p:WindowsPackageType=MSIX -p:GenerateAppxPackageOnBuild=true `
        -p:AppxPackageSigningEnabled=false -p:AppxBundle=Never -p:UapAppxPackageBuildMode=SideloadOnly `
        -p:AppxPackageDir="$out\" -nologo -v:minimal
    if ($LASTEXITCODE) { throw "dotnet publish ($arch) failed" }
    $msix = Get-ChildItem $out -Recurse -Filter *.msix | Where-Object { $_.Name -notlike '*Dependencies*' -and $_.DirectoryName -notlike '*Dependencies*' } | Select-Object -First 1
    Copy-Item $msix.FullName "$Repo\releases\Concentration-$version-windows-$arch.msix" -Force
    Copy-Item $msix.FullName "$Repo\artifacts\windows-test\Concentration-$version-windows-$arch.msix" -Force
    Write-Host "  releases\Concentration-$version-windows-$arch.msix"
}

# the test copies are signed with a self-signed certificate whose subject is the Store publisher,
# so they install on this PC once the certificate is trusted (tools/windows-test.ps1 does that)
$publisher = 'CN=A6EAEB04-6634-41C1-BDFE-695819ECE444'
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object { $_.Subject -eq $publisher } | Select-Object -First 1
if (-not $cert) {
    $cert = New-SelfSignedCertificate -Type Custom -Subject $publisher -KeyUsage DigitalSignature -FriendlyName 'Concentration test signing' `
        -CertStoreLocation Cert:\CurrentUser\My -TextExtension @('2.5.29.37={text}1.3.6.1.5.5.7.3.3', '2.5.29.19={text}')
}
Export-Certificate -Cert $cert -FilePath "$Repo\artifacts\windows-test\test-signing.cer" | Out-Null
$signtool = Get-ChildItem "$env:USERPROFILE\.nuget\packages\microsoft.windows.sdk.buildtools" -Recurse -Filter signtool.exe |
    Where-Object { $_.DirectoryName -like '*\x64' } | Sort-Object FullName -Descending | Select-Object -First 1
foreach ($arch in $Archs) {
    & $signtool.FullName sign /fd SHA256 /sha1 $cert.Thumbprint "$Repo\artifacts\windows-test\Concentration-$version-windows-$arch.msix" | Out-Null
    if ($LASTEXITCODE) { throw "signtool ($arch) failed" }
}
Write-Host "  artifacts\windows-test: signed test copies and test-signing.cer"
