param([Parameter(Mandatory)][string]$BepInExRoot)
$ErrorActionPreference = 'Stop'
if (Get-Process PEAK -ErrorAction SilentlyContinue | Where-Object { $_.Threads.Count -gt 0 }) { throw 'Exit PEAK first.' }
$profileRoot = (Resolve-Path -LiteralPath $BepInExRoot).Path
$plugins = Join-Path $profileRoot 'plugins'
$cecil = Join-Path $profileRoot 'core\Mono.Cecil.dll'
if (!(Test-Path -LiteralPath $cecil) -or !(Test-Path -LiteralPath $plugins)) { throw 'Specify an installed BepInEx directory, not the game or drive root.' }
$candidates = @(Get-ChildItem -LiteralPath $plugins -Recurse -Filter MoreCustomizations.dll -File)
if ($candidates.Count -ne 1) { throw 'Exactly one installed MoreCustomizations.dll is required.' }
$framework = $candidates[0].FullName
$backup = Join-Path $profileRoot 'JojoHats-backup'
New-Item -ItemType Directory -Force $backup | Out-Null
$original = Join-Path $backup 'MoreCustomizations.original.dll'
if (!(Test-Path -LiteralPath $original)) { Copy-Item -LiteralPath $framework -Destination $original }
& "$PSScriptRoot\allow-empty-bundles.ps1" -SourceDll $original -OutputDll $framework -CecilDll $cecil
$sample = Join-Path $candidates[0].DirectoryName 'built-in.pcab'
if (Test-Path -LiteralPath $sample) {
    $resolved = (Resolve-Path -LiteralPath $sample).Path
    if (!$resolved.StartsWith($plugins + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Sample path escaped plugin directory.' }
    $sampleBackup = Join-Path $backup ('built-in-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.pcab')
    Move-Item -LiteralPath $resolved -Destination $sampleBackup
}
Write-Output "JOJO-only compatibility installed. Original framework/sample backup: $backup"
Write-Output 'Install the adjacent JojoHats DLL/assets from the release ZIP if not already installed. Vanilla cosmetics are unchanged.'
