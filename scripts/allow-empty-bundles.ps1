param([Parameter(Mandatory)][string]$SourceDll, [Parameter(Mandatory)][string]$OutputDll, [Parameter(Mandatory)][string]$CecilDll)
$ErrorActionPreference = 'Stop'
if ([IO.Path]::GetFullPath($SourceDll) -eq [IO.Path]::GetFullPath($OutputDll)) { throw 'A separate output is required; preserve the original.' }
Add-Type -Path $CecilDll
$assembly = [Mono.Cecil.AssemblyDefinition]::ReadAssembly($SourceDll)
try {
    $type = @($assembly.MainModule.Types | Where-Object FullName -eq 'MoreCustomizations.MoreCustomizationsPlugin')
    if ($type.Count -ne 1) { throw 'Unsupported framework type.' }
    $method = @($type[0].Methods | Where-Object Name -eq 'LoadAllCustomizations')
    if ($method.Count -ne 1) { throw 'Unsupported framework loader.' }
    $instructions = $method[0].Body.Instructions
    $errorInstruction = @($instructions | Where-Object { $_.OpCode -eq [Mono.Cecil.Cil.OpCodes]::Ldstr -and $_.Operand -eq "No customization files found in '" })
    if ($errorInstruction.Count -ne 1) { throw 'Unknown or already-patched framework. Use the untouched vendor DLL.' }
    $index = $instructions.IndexOf($errorInstruction[0])
    $guard = $instructions[$index - 1]
    if ($guard.OpCode -ne [Mono.Cecil.Cil.OpCodes]::Brtrue_S -or $instructions[$index-2].OpCode -ne [Mono.Cecil.Cil.OpCodes]::Ldlen -or $instructions[$index-3].OpCode -ne [Mono.Cecil.Cil.OpCodes]::Ldloc_1 -or $guard.Operand.Previous.OpCode -ne [Mono.Cecil.Cil.OpCodes]::Throw) { throw 'Unsupported framework IL; no output written.' }
    $instructions[$index-3].OpCode = [Mono.Cecil.Cil.OpCodes]::Nop
    $instructions[$index-3].Operand = $null
    $instructions[$index-2].OpCode = [Mono.Cecil.Cil.OpCodes]::Nop
    $instructions[$index-2].Operand = $null
    $guard.OpCode = [Mono.Cecil.Cil.OpCodes]::Br_S
    $assembly.Write($OutputDll)
    Write-Output 'PASS: empty bundle list allowed; normal framework loading and patches preserved.'
} finally { $assembly.Dispose() }
