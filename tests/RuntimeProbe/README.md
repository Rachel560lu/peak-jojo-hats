# Isolated runtime catalog probe

Test-only BepInEx plugin. **Do not include this DLL in a player installation or release ZIP.**

It reads More Customizations' registered asset catalog after an explicit 18-second startup wait. It does not change catalogs, assets, configuration, player selections, saves, Steam, or network state. The only file it writes is `BepInEx/jojo-probe.txt` in the selected test profile.

Build with the same local reference properties as the main project:

```powershell
dotnet build tests/RuntimeProbe/RuntimeProbe.csproj -c Release `
  "-p:PeakManagedDir=<PEAK>/PEAK_Data/Managed" `
  "-p:BepInExCoreDir=<isolated-profile>/BepInEx/core" `
  "-p:MoreCustomizationsDll=<isolated-profile>/BepInEx/plugins/MoreCustomizations/MoreCustomizations.dll"
```

Copy only `bin/Release/netstandard2.1/JojoHats.RuntimeProbe.dll` into the isolated profile's plugins directory. Local game/framework assemblies are references only; this project has no NuGet dependencies.

Launch arguments:

```text
--jojo-probe-test --jojo-probe-expect-jojo=6 --jojo-test-quit
```

Use `--jojo-probe-expect-jojo=0` for the baseline, an intentionally broken own-asset initialization test, or the uninstalled case. The expected argument is mandatory when the probe is enabled. `--jojo-test-quit` is optional and is the only condition under which the probe quits the application. Without `--jojo-probe-test`, the plugin is inert.

The result records `frameworkInitialized=True/False`, category counts, `customHatEntries`, `customNonHatEntries`, `jojoCount`, and `result=PASS` or `result=FAIL`. The `orderedNames=` value is JSON that preserves catalog/category entry order. The single-line `foreignCatalog=` JSON signature excludes JOJO names, sorts category keys ordinally, and preserves entry order within each category. Empty foreign categories are omitted so appending an otherwise absent Hat category cannot change the signature of pre-existing entries. Individual category counts remain available separately.

Registration names are asset identities; no player data is inspected. PASS verifies the explicit JOJO count, Hat-only registration, and the expected order of the six names. It does **not** imply multiplayer or interactive UI verification.
