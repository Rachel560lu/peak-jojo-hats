param(
    [Parameter(Mandatory)][string]$GameDir,
    [Parameter(Mandatory)][string]$BepInExRoot,
    [string]$MoreCustomizationsDll,
    [string]$Dotnet = 'dotnet'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$gameRoot = (Resolve-Path -LiteralPath $GameDir).Path
$frameworkRoot = (Resolve-Path -LiteralPath $BepInExRoot).Path
$managedDir = Join-Path $gameRoot 'PEAK_Data\Managed'
$coreDir = Join-Path $frameworkRoot 'core'

if ([string]::IsNullOrWhiteSpace($MoreCustomizationsDll)) {
    $pluginsDir = Join-Path $frameworkRoot 'plugins'
    if (!(Test-Path -LiteralPath $pluginsDir -PathType Container)) {
        throw 'BepInExRoot must contain plugins, or supply -MoreCustomizationsDll explicitly.'
    }
    $candidates = @(Get-ChildItem -LiteralPath $pluginsDir -Filter 'MoreCustomizations.dll' -Recurse -File)
    if ($candidates.Count -ne 1) {
        throw 'Expected exactly one MoreCustomizations.dll under BepInEx/plugins. Supply its path explicitly with -MoreCustomizationsDll.'
    }
    $MoreCustomizationsDll = $candidates[0].FullName
}
$customizationsDll = (Resolve-Path -LiteralPath $MoreCustomizationsDll).Path
$requiredFiles = @(
    (Join-Path $gameRoot 'PEAK.exe'),
    (Join-Path $managedDir 'Assembly-CSharp.dll'),
    (Join-Path $managedDir 'UnityEngine.dll'),
    (Join-Path $managedDir 'UnityEngine.CoreModule.dll'),
    (Join-Path $managedDir 'UnityEngine.JSONSerializeModule.dll'),
    (Join-Path $managedDir 'UnityEngine.ImageConversionModule.dll'),
    (Join-Path $coreDir 'BepInEx.dll'),
    (Join-Path $coreDir '0Harmony.dll'),
    $customizationsDll
)
foreach ($requiredFile in $requiredFiles) {
    if (!(Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "Required local build reference not found: $requiredFile"
    }
}
if (!(Get-Command $Dotnet -CommandType Application -ErrorAction SilentlyContinue)) {
    throw 'Install the .NET 8 SDK and put dotnet on PATH, or supply -Dotnet with its executable path.'
}

$previousDotnetHome = $env:DOTNET_CLI_HOME
$previousTelemetry = $env:DOTNET_CLI_TELEMETRY_OPTOUT
$previousCertificate = $env:DOTNET_GENERATE_ASPNET_CERTIFICATE
$previousToolsPath = $env:DOTNET_ADD_GLOBAL_TOOLS_TO_PATH
try {
    $env:DOTNET_CLI_HOME = Join-Path $projectRoot '.dotnet-home'
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    $env:DOTNET_GENERATE_ASPNET_CERTIFICATE = 'false'
    $env:DOTNET_ADD_GLOBAL_TOOLS_TO_PATH = 'false'
    & $Dotnet build (Join-Path $projectRoot 'JojoHats.csproj') -c Release `
        "-p:PeakManagedDir=$managedDir" "-p:BepInExCoreDir=$coreDir" `
        "-p:MoreCustomizationsDll=$customizationsDll"
    if ($LASTEXITCODE -ne 0) { throw 'Build failed.' }
} finally {
    $env:DOTNET_CLI_HOME = $previousDotnetHome
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = $previousTelemetry
    $env:DOTNET_GENERATE_ASPNET_CERTIFICATE = $previousCertificate
    $env:DOTNET_ADD_GLOBAL_TOOLS_TO_PATH = $previousToolsPath
}
Write-Output 'Build complete: bin/Release/netstandard2.1/JojoHats.dll'
Write-Output 'Local game and framework assemblies were referenced only, not redistributed.'
