param(
    [Parameter(Mandatory)][string]$PreparedProfile,
    [Parameter(Mandatory)][string]$GameDir,
    [Parameter(Mandatory)][string]$ReleaseDll,
    [Parameter(Mandatory)][string]$LegacyZip
)
$ErrorActionPreference = 'Stop'
$project = Split-Path $PSScriptRoot -Parent
$base = [IO.Path]::GetFullPath((Join-Path $project 'test-profile'))
$source = (Resolve-Path -LiteralPath $PreparedProfile).Path
if (!$source.StartsWith($base + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Source must be a generated project test profile, not a player profile.'
}
if (Get-Process PEAK -ErrorAction SilentlyContinue) { throw 'Close PEAK first.' }
$root = Join-Path $base ('lifecycle-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root | Out-Null
Copy-Item -LiteralPath (Join-Path $source 'runtime') -Destination $root -Recurse
$runtime = Join-Path $root 'runtime'
$bep = Join-Path $runtime 'BepInEx'
$plugins = Join-Path $bep 'plugins'
$jojo = Join-Path $plugins 'Rachel560lu-JojoScoutHats'
$disabled = Join-Path $root 'disabled-JOJO'
# Validate both exact targets before moving the directory, even within a test profile.
foreach ($path in @($jojo, $disabled)) {
    if (![IO.Path]::GetFullPath($path).StartsWith($root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Lifecycle move target escaped the generated test profile.'
    }
}
$probeSource = Join-Path $project 'tests/RuntimeProbe/bin/Release/netstandard2.1/JojoHats.RuntimeProbe.dll'
if (!(Test-Path -LiteralPath $probeSource)) { throw 'Build tests/RuntimeProbe first.' }
$probeDir = Join-Path $plugins 'JOJO-Test-Probe'
New-Item -ItemType Directory -Path $probeDir | Out-Null
Copy-Item -LiteralPath $probeSource -Destination $probeDir
$protected = @(Get-ChildItem -LiteralPath $plugins -Recurse -File | Where-Object {
    !$_.FullName.StartsWith($jojo + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
})
$hashes = @{}
foreach ($file in $protected) { $hashes[$file.FullName] = (Get-FileHash -LiteralPath $file.FullName).Hash }

function Invoke-Probe([string]$Stage, [int]$ExpectedJojo) {
    $resultPath = Join-Path $bep 'jojo-probe.txt'
    if (Test-Path -LiteralPath $resultPath) {
        Move-Item -LiteralPath $resultPath -Destination (Join-Path $root ('previous-' + $Stage + '-probe.txt'))
    }
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = Join-Path $GameDir 'PEAK.exe'
    $start.WorkingDirectory = $GameDir
    $start.UseShellExecute = $false
    $start.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.EnvironmentVariables['SteamAppId'] = '3527290'
    $start.EnvironmentVariables['SteamGameId'] = '3527290'
    $start.Arguments = '--doorstop-enabled true --doorstop-target-assembly "' + (Join-Path $bep 'core/BepInEx.Preloader.dll') +
        '" -logFile "' + (Join-Path $root ($Stage + '-Player.log')) +
        '" -batchmode -nographics --jojo-probe-test --jojo-test-quit --jojo-probe-expect-jojo=' + $ExpectedJojo
    $process = [Diagnostics.Process]::Start($start)
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()
    Write-Host "STAGE=$Stage PID=$($process.Id)"
    $deadline = [DateTime]::UtcNow.AddSeconds(90)
    while (!$process.WaitForExit(500) -and [DateTime]::UtcNow -lt $deadline) { }
    if (!$process.HasExited) { throw "Probe timed out; process $($process.Id) remains for inspection." }
    if ($process.ExitCode -ne 0 -or !(Test-Path -LiteralPath $resultPath)) { throw 'Probe did not complete successfully.' }
    $lines = Get-Content -LiteralPath $resultPath
    if ($lines -notcontains 'result=PASS') { throw ($lines -join "`n") }
    foreach ($file in $protected) {
        if (!(Test-Path -LiteralPath $file.FullName) -or (Get-FileHash -LiteralPath $file.FullName).Hash -ne $hashes[$file.FullName]) {
            throw 'A protected dependency/other mod changed during lifecycle test.'
        }
    }
    Copy-Item -LiteralPath $resultPath -Destination (Join-Path $root ($Stage + '-result.txt'))
    Write-Host ($lines | Where-Object { $_ -match '^(frameworkInitialized|jojoCount|customHatEntries|customNonHatEntries|result)=' })
    return @($lines | Where-Object { $_.StartsWith('foreignCatalog=') })[0]
}

Write-Host "PROFILE=$root"
Move-Item -LiteralPath $jojo -Destination $disabled
$baseline = Invoke-Probe 'baseline' 0
Move-Item -LiteralPath $disabled -Destination $jojo
$installedDll = Join-Path $jojo 'JojoHats/JojoHats.dll'
Copy-Item -LiteralPath $ReleaseDll -Destination $installedDll -Force
if ((Invoke-Probe 'installed' 6) -ne $baseline) { throw 'Foreign catalog changed on install.' }

# Simulate a missing/corrupted own resource via a recoverable move, never touching foreign files.
$mesh = Join-Path $jojo 'JojoHats/assets/06_joseph_hair/mesh.json'
$meshBackup = Join-Path $root 'joseph-mesh.json'
Move-Item -LiteralPath $mesh -Destination $meshBackup
if ((Invoke-Probe 'missing-own-asset' 0) -ne $baseline) { throw 'Foreign catalog changed on own asset failure.' }
Move-Item -LiteralPath $meshBackup -Destination $mesh

# Icon loading fails after a CustomHat object has been allocated; this must also
# leave the whole foreign catalog intact rather than publishing partial hats.
$icon = Join-Path $jojo 'JojoHats/assets/05_jolyne_buns/icon.png'
$iconBackup = Join-Path $root 'jolyne-icon.png'
Move-Item -LiteralPath $icon -Destination $iconBackup
if ((Invoke-Probe 'missing-own-icon' 0) -ne $baseline) { throw 'Foreign catalog changed on own icon failure.' }
Move-Item -LiteralPath $iconBackup -Destination $icon

# Exercise replacement of the actual old plugin binary. No Steam selection is changed.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$legacy = [IO.Compression.ZipFile]::OpenRead((Resolve-Path -LiteralPath $LegacyZip).Path)
try {
    $entry = $legacy.GetEntry('BepInEx/plugins/JojoHats/JojoHats.dll')
    if (!$entry) { throw 'Legacy archive does not contain the expected JOJO DLL.' }
    [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $installedDll, $true)
} finally { $legacy.Dispose() }
$legacyCatalog = Invoke-Probe 'legacy-0.4.2' 6
Copy-Item -LiteralPath $ReleaseDll -Destination $installedDll -Force
if ((Invoke-Probe 'upgraded-0.5.0' 6) -ne $baseline) { throw 'Foreign catalog not restored by additive upgrade.' }
Move-Item -LiteralPath $jojo -Destination $disabled
if ((Invoke-Probe 'uninstalled' 0) -ne $baseline) { throw 'Foreign catalog changed after uninstall.' }
Write-Host 'LIFECYCLE=PASS; baseline/install/missing-own-resource/missing-own-icon/legacy-binary/upgrade/uninstall; foreign catalog and dependency hashes preserved by v0.5.0'
Write-Host 'Saved-hat selection and two-client multiplayer were not exercised. Old v0.4.2 intentionally hides foreign cosmetics.'
