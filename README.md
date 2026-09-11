<p align="center">
  <img src="docs/banner/peak-jojo-hats-header-v1.png" width="100%" alt="Six PEAK-style JOJO scouts surrounding the peak-jojo-hats title / 六位 PEAK 版 JOJO 围绕模组标题">
</p>

<h1 align="center">peak-jojo-hats</h1>

<p align="center">
  <strong>JOJO's Bizarre Climb</strong><br>
  JOJO-inspired hats and hairstyles for PEAK.
</p>

<p align="center">
  <strong>JOJO 的奇妙登山</strong><br>
  给 PEAK 小人换个 JOJO 发型。
</p>

<p align="center">
  <a href="https://thunderstore.io/c/peak/p/Rachel560lu/JojoScoutHats/"><img src="https://img.shields.io/badge/Download-Thunderstore-a4d56e?style=for-the-badge&amp;labelColor=555555" alt="Download on Thunderstore / 在 Thunderstore 下载"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/Version-v0.5.0-405c68?style=for-the-badge&amp;labelColor=555555" alt="Version 0.5.0"></a>
  <a href="docs/INSTALL.md"><img src="https://img.shields.io/badge/BepInEx-5-405c68?style=for-the-badge&amp;labelColor=555555" alt="Requires BepInEx 5"></a>
  <img src="https://img.shields.io/badge/Hats-6-7560a8?style=for-the-badge&amp;labelColor=555555" alt="Six head cosmetics / 六款头饰">
</p>

<p align="center">
  <a href="https://thunderstore.io/c/peak/p/Rachel560lu/JojoScoutHats/">Download / 下载</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.md">English</a> ·
  <a href="docs/INSTALL.md">Install / 安装</a> ·
  <a href="https://github.com/Rachel560lu/peak-jojo-hats/issues">Report an issue / 反馈</a>
</p>

A small JOJO fan mod for **PEAK**. Pick from six looks inspired by Jonathan, Joseph, Jotaro, Josuke, Giorno and Jolyne, then head out for a climb. They're all worn as hats, including the hairstyles.

> **Just hats and hair.** The eyes, expressions, outfits and props in the screenshots aren't included. This mod only changes your headwear—no extra abilities, body replacements or moving hair.

## In-game gallery

Here's how they look in-game. Click a photo for a closer look.

<table>
<tr><th>Jonathan Joestar</th><th>Joseph Joestar</th><th>Jotaro Kujo</th></tr>
<tr>
<td><a href="docs/images/jonathan.png"><img src="docs/images/jonathan.png" width="280" alt="Jonathan's blue rising hairstyle in PEAK, four gameplay poses"></a></td>
<td><a href="docs/images/joseph.png"><img src="docs/images/joseph.png" width="280" alt="Joseph's swept brown hair and patterned headband in PEAK"></a></td>
<td><a href="docs/images/jotaro.png"><img src="docs/images/jotaro.png" width="280" alt="Jotaro's black cap with gold emblems and attached hair in PEAK"></a></td>
</tr>
<tr><th>Josuke Higashikata</th><th>Giorno Giovanna</th><th>Jolyne Cujoh</th></tr>
<tr>
<td><a href="docs/images/josuke.png"><img src="docs/images/josuke.png" width="280" alt="Josuke's indigo pompadour in PEAK"></a></td>
<td><a href="docs/images/giorno.png"><img src="docs/images/giorno.png" width="280" alt="Giorno's golden three-roll hairstyle and braid in PEAK"></a></td>
<td><a href="docs/images/jolyne.png"><img src="docs/images/jolyne.png" width="280" alt="Jolyne's navy twin buns, lime bangs and braid in PEAK"></a></td>
</tr>
</table>

## What's included

- Six selectable hats: Jotaro Cap, Josuke Pompadour, Giorno Rolls, Jonathan Hair, Jolyne Buns and Joseph Hair.
- Adds to your existing cosmetics: keep your other custom hats, eyes, faces and accessories.
- Rounded shapes and simple colors to suit PEAK's little scouts.
- Pick your favorite in the passport's Hat tab, with BepInEx and More Customizations installed.
- Want to tinker? Model files are included. You don't need Blender or Unity Editor just to play.

## Install

1. Open [JojoScoutHats on Thunderstore](https://thunderstore.io/c/peak/p/Rachel560lu/JojoScoutHats/) and install **v0.5.0 or newer** with r2modman or Thunderstore Mod Manager. Accept the dependency installation.
2. Start **modded PEAK** from the manager.
3. Open the passport's **Hat** tab and choose a JOJO icon.

No PowerShell, file deletion or framework patch is needed. Leave More Customizations and its included `built-in.pcab` as installed. Dependencies: BepInExPack_PEAK **5.4.75301** and More Customizations **1.1.10**. See [the installation guide](docs/INSTALL.md) for manual installation and troubleshooting.

**Coming from v0.4.2?** Equip a vanilla hat before upgrading, then reselect your JOJO hat afterward: the old exclusive catalog and the new shared catalog can use different positions. If you previously ran the JOJO-only patch or removed the framework's sample bundle, a **fresh mod-manager profile** is the simplest way to start clean. Updating this mod does not restore or modify third-party files.

### Compatibility notes

- v0.5.0 appends six hats; it does not replace other custom categories, delete bundles or patch dependency DLLs. Vanilla cosmetics remain available too.
- For multiplayer, share the **same complete cosmetic profile**, including dependencies, all other cosmetic packs and their versions. Installing only the same JOJO version is not enough. Models are not transferred between players; two-client appearance and reconnect validation are still pending.
- Switch to a vanilla hat before uninstalling or launching an unmodded profile.
- The supported framework target is unmodified More Customizations 1.1.10. Other framework or game versions may need a compatibility update; see [validation scope](docs/VALIDATION.md).
- These are static hats. Clipping with every outfit, first-person camera and climbing/ragdoll pose has not been exhaustively tested.

## Source and development

Current version: **0.5.0**. The six models are unchanged from v0.4.2; this update focuses on installation and coexistence with other cosmetics. The repository includes the C# loader, procedural model sources, exported JSON/OBJ meshes, shared palette and the six original-size showcase images.

See [Build and model development](docs/BUILD.md), [validation scope](docs/VALIDATION.md) and [changelog](CHANGELOG.md). Game assemblies and third-party mod DLLs are **not** distributed here; a local PEAK installation is needed to compile the loader.

## Credits and project status

The header is a promotional illustration; the six gallery images are actual gameplay screenshots.

Thanks to [BepInEx](https://github.com/BepInEx/BepInEx) and [More Customizations](https://github.com/Creta5164/peak-more-customizations) for making custom cosmetics possible, and to the [hat-making guide](https://github.com/Creta5164/peak-more-customizations/blob/main/docs/hat.md) for the setup reference.

This is an unofficial fan project, not affiliated with or endorsed by the creators or rights holders of PEAK or JoJo's Bizarre Adventure. The mod meshes were authored for this project; screenshots contain the game and its existing cosmetics. No explicit reuse license is included yet—please contact the maintainer before reusing project material.
