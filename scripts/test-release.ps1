param(
    [Parameter(Mandatory)][string]$PackageZip,
    [Parameter(Mandatory)][string]$GameDir,
    [ValidateSet('clean', 'mixed')][string]$Scenario = 'clean',
    [switch]$PrepareOnly
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$package = (Resolve-Path -LiteralPath $PackageZip).Path
$game = (Resolve-Path -LiteralPath $GameDir).Path
if (!(Test-Path -LiteralPath (Join-Path $game 'PEAK.exe'))) { throw 'GameDir must contain PEAK.exe.' }
if (Get-Process PEAK -ErrorAction SilentlyContinue) { throw 'Close PEAK before running an isolated test.' }

# Always create a new profile: never repair or reuse a player's installation.
$testBase = Join-Path $projectRoot 'test-profile'
New-Item -ItemType Directory -Force -Path $testBase | Out-Null
$testRoot = Join-Path $testBase ($Scenario + '-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $testRoot | Out-Null
$downloads = Join-Path $testRoot 'downloads'
New-Item -ItemType Directory -Path $downloads | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Expand-SafeZip([string]$ZipPath, [string]$Destination) {
    $root = [IO.Path]::GetFullPath($Destination)
    if (!$root.StartsWith($testRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Extraction must stay within this newly created test profile.'
    }
    $archive = [IO.Compression.ZipFile]::OpenRead($ZipPath)
    try {
        foreach ($entry in $archive.Entries) {
            $target = [IO.Path]::GetFullPath((Join-Path $root $entry.FullName))
            if (!$target.StartsWith($root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
                throw 'Unsafe archive member path.'
            }
        }
    } finally { $archive.Dispose() }
    [IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $root)
}

function Fetch-Package([string]$Name, [string]$Url) {
    $zip = Join-Path $downloads ($Name + '.zip')
    Invoke-WebRequest -Uri $Url -OutFile $zip
    $folder = Join-Path $downloads $Name
    Expand-SafeZip $zip $folder
    return $folder
}

$bep = Fetch-Package 'BepInEx' 'https://thunderstore.io/package/download/BepInEx/BepInExPack_PEAK/5.4.75301/'
$mc = Fetch-Package 'MoreCustomizations' 'https://thunderstore.io/package/download/cretapark/More_Customizations/1.1.10/'
$runtime = Join-Path $testRoot 'runtime'
New-Item -ItemType Directory -Path $runtime | Out-Null
Copy-Item -LiteralPath (Join-Path $bep 'BepInExPack_PEAK/BepInEx') -Destination $runtime -Recurse
$plugins = Join-Path $runtime 'BepInEx/plugins'
# Team-prefixed manager-style folder plus embedded plugin folder: runtime must be path-portable.
$mcInstall = Join-Path $plugins 'cretapark-More_Customizations'
New-Item -ItemType Directory -Path $mcInstall | Out-Null
Copy-Item -LiteralPath (Join-Path $mc 'BepInEx/plugins/MoreCustomizations') -Destination $mcInstall -Recurse
if ($Scenario -eq 'mixed') {
    $uma = Fetch-Package 'Umamusume' 'https://thunderstore.io/package/download/Arcavian/Umamusume_Hats/0.1.1/'
    $umaInstall = Join-Path $plugins 'Arcavian-Umamusume_Hats'
    New-Item -ItemType Directory -Path $umaInstall | Out-Null
    Copy-Item -LiteralPath (Join-Path $uma 'umamusume-hats.pcab') -Destination $umaInstall
}
$ownExtract = Join-Path $downloads 'JOJO'
Expand-SafeZip $package $ownExtract
$ownInstall = Join-Path $plugins 'Rachel560lu-JojoScoutHats'
New-Item -ItemType Directory -Path $ownInstall | Out-Null
Copy-Item -LiteralPath (Join-Path $ownExtract 'BepInEx/plugins/JojoHats') -Destination $ownInstall -Recurse

# Only test-local hashes; nothing is written to the game directory or existing mod profiles.
$protected = @(Get-ChildItem -LiteralPath $mcInstall -Recurse -File)
if ($Scenario -eq 'mixed') { $protected += @(Get-ChildItem -LiteralPath $umaInstall -Recurse -File) }
$before = @{}
foreach ($file in $protected) { $before[$file.FullName] = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash }
Write-Output "PROFILE=$testRoot"
if ($PrepareOnly) { return }

$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = Join-Path $game 'PEAK.exe'
$start.WorkingDirectory = $game
$start.UseShellExecute = $false
$start.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
$start.RedirectStandardOutput = $true
$start.RedirectStandardError = $true
$start.EnvironmentVariables['SteamAppId'] = '3527290'
$start.EnvironmentVariables['SteamGameId'] = '3527290'
$preloader = Join-Path $runtime 'BepInEx/core/BepInEx.Preloader.dll'
$resultPath = Join-Path $runtime 'BepInEx/jojo-smoke.txt'
for ($run = 1; $run -le 2; $run++) {
    if (Test-Path -LiteralPath $resultPath) {
        Move-Item -LiteralPath $resultPath -Destination (Join-Path $testRoot ('before-run-' + $run + '-smoke.txt'))
    }
    $log = Join-Path $testRoot ('Player-' + $run + '.log')
    $start.Arguments = '--doorstop-enabled true --doorstop-target-assembly "' + $preloader + '" -logFile "' + $log + '" -batchmode -nographics --jojo-smoke-test --jojo-test-quit'
    $process = [Diagnostics.Process]::Start($start)
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()
    Write-Output "RUN=$run PID=$($process.Id)"
    # Short polling allows the calling terminal/tool to yield while the test runs.
    $deadline = [DateTime]::UtcNow.AddSeconds(90)
    while (!$process.WaitForExit(500) -and [DateTime]::UtcNow -lt $deadline) { }
    if (!$process.HasExited) { throw "Test timed out; process $($process.Id) remains running for inspection." }
    if ($process.ExitCode -ne 0) { throw "PEAK exited with $($process.ExitCode). Inspect $log" }
    if (!(Test-Path -LiteralPath $resultPath)) { throw "No smoke result. Inspect $log" }
    $result = Get-Content -LiteralPath $resultPath
    $result
    Copy-Item -LiteralPath $resultPath -Destination (Join-Path $testRoot ('result-' + $run + '.txt'))
    if ($result -notcontains 'result=PASS') { throw "Runtime verification failed. Inspect $log" }
    $expectedVersion = (Get-Content -LiteralPath (Join-Path $ownExtract 'manifest.json') -Raw | ConvertFrom-Json).version_number
    if ($result -notcontains ('version=' + $expectedVersion)) { throw 'Wrong runtime version loaded.' }
    foreach ($file in $protected) {
        if (!(Test-Path -LiteralPath $file.FullName) -or (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash -ne $before[$file.FullName]) {
            throw 'A dependency or other cosmetic file was modified.'
        }
    }
    Write-Output "RUN=$run protectedDependencyHashes=PASS"
}
Write-Output "SCENARIO=$Scenario RESULT=PASS (package extraction + Unity smoke + restart, not a mod-manager UI or two-client test)"
