# Building JOJO Scout Hats

This repository contains the plugin source, editable OBJ models and runtime JSON
meshes. Unity Editor is not needed to build or load this mod. Do not redistribute
PEAK, Unity or dependency assemblies with your builds.

## Local prerequisites

- Windows and PowerShell.
- The .NET 8 SDK (`dotnet --list-sdks` should list an 8.x SDK).
- Your own installed copy of PEAK, including `PEAK_Data/Managed`.
- A local BepInEx PEAK profile with BepInEx core assemblies and More Customizations
  **1.1.10** installed. The plugin uses that version's `CustomHat_V1` API and a
  narrow reflection bridge; other framework versions are not validated.

The build uses these files as read-only references. It does not install mods,
modify the game, patch More Customizations or launch PEAK.

## Compile the plugin

From the repository root, substitute your actual installation/profile paths:

```powershell
.\scripts\build.ps1 -GameDir 'YOUR_PEAK_DIRECTORY' -BepInExRoot 'YOUR_PROFILE\BepInEx'
```

The script discovers exactly one `MoreCustomizations.dll` under that profile's
`plugins` directory. To use a specific local dependency, add:

```powershell
-MoreCustomizationsDll 'YOUR_DEPENDENCY_DIRECTORY\MoreCustomizations.dll'
```

If the SDK is not on PATH, add `-Dotnet 'YOUR_SDK_DIRECTORY\dotnet.exe'`.
All required assembly paths are checked before the build. The project has no
personal-machine path defaults and no NuGet package dependencies.

Output is `bin/Release/netstandard2.1/JojoHats.dll`. References have
`Private="false"`, so game and framework DLLs are not copied to the output.
Release debug symbols are disabled to avoid embedding a private local PDB path
in the distributed DLL.
Build intermediates and CLI state remain in the repository's ignored `bin`,
`obj` and `.dotnet-home` directories. Keep the compiled DLL beside its `assets`
directory when installing; see the main README for the separate installation
and zero-PCAB compatibility steps.

## Models and validation

The committed JSON files are the runtime assets. Their coordinates use Unity
axes; OBJ authoring coordinates use +Y forward and +Z up. The guide head radius
is 1.415 authoring units, not an exported game character.

Model tooling uses Python 3, NumPy and Pillow. On Windows, with those packages
available in your Python environment:

```powershell
python -m pip install -r requirements.txt
python tools/refine_models_v42.py
python tools/validate_assets.py
```

The v0.4.2 exporter updates only Jotaro, Giorno, Jonathan and Joseph. Josuke and
Jolyne retain the committed **v0.4.1** assets, and the shared palette is frozen.
Do not run the legacy `generate_models.py` or `upgrade_models.py` entry points
over the release assets: they describe older
stages, not a full current release rebuild. Current helpers import those modules
for geometry primitives and rendering.

Validation checks mesh indices, normals, palette UVs, icons, OBJ/JSON coordinate
parity and preservation of the two frozen hats. Offline previews use the actual
exported meshes on a guide head; they are not proof of gameplay fit or multiplayer
compatibility. In-game visual testing remains a separate step.

`tools/import_blender.py` is optional: run it in Blender's Scripting workspace to
make a local scene from the committed runtime meshes. Blender and Unity Editor
are not prerequisites for compiling the plugin or regenerating its JSON assets.

Current six-view and turntable previews are generated into `docs/model-v42` and
are ignored by Git. Before/after sheets require optional local historical assets
under `backups/pre-refinement-v0.4.2/assets`; those backups are not in this repo.

## Package a release

After building Release and validating the assets:

```powershell
python tools/package.py
```

This creates `dist/JojoScoutHats-0.4.2.zip` from an explicit runtime allowlist:
the project's DLL, six meshes/icons, shared palette/catalog, metadata and the
compatibility scripts. It does not include game/framework DLLs, OBJ sources,
screenshots, development logs or local paths. The archive README uses absolute
repository links so documentation works outside a source checkout.
