# JOJO Scout Hats for PEAK

Six JOJO-inspired head cosmetics: Jotaro Cap, Josuke Pompadour, Giorno Rolls,
Jonathan Hair, Jolyne Buns and Joseph Hair. Version 0.4.2.

[Screenshots and source](https://github.com/Rachel560lu/peak-jojo-hats) ·
[中文介绍](https://github.com/Rachel560lu/peak-jojo-hats/blob/main/README.zh-CN.md) ·
[Full installation guide](https://github.com/Rachel560lu/peak-jojo-hats/blob/main/docs/INSTALL.md)

## Install

Use a **dedicated PEAK profile**, with the tested dependencies:

- BepInEx-BepInExPack_PEAK-5.4.75301
- cretapark-More_Customizations-1.1.10

Close PEAK. Copy `BepInEx/plugins/JojoHats` to your profile's `BepInEx/plugins`,
keeping the complete `assets` directory beside the DLL.
From this extracted ZIP root, open PowerShell and run:

```powershell
.\scripts\install-jojo-only.ps1 -BepInExRoot 'FULL_PATH_TO_PROFILE\BepInEx'
```

Replace the placeholder with your actual profile path. The script backs up the
local framework DLL, patches its empty-bundle check, and moves `built-in.pcab`
out of the loading path. Backups are in `BepInEx/JojoHats-backup`. Simply deleting
the sample is insufficient. The patch is tested only with 1.1.10; do not reuse
an old backup across framework updates. See the full guide before modifying a
profile. No game/framework DLL is bundled here.

Launch modded PEAK and select a JOJO icon in the passport's Hat tab.

## Important

This replaces the **custom** cosmetic catalog with six hats. Vanilla cosmetics
remain available; other custom eyes, hats and accessories are excluded.
The screenshots' eyes, outfits and props are not added by this mod.
All hats are static. Multiplayer has not been validated with two clients.
Equip a vanilla hat before uninstalling or using an unmodded profile.

这是仅头饰的 JOJO 同人模组。请使用独立配置，保留完整资源目录，并运行兼容脚本；
不能只删除 built-in.pcab。模组不增加眼睛或服装，会隐藏其他自定义外观，但保留原版。
详细中文说明及六张实机展示请访问上面的项目链接。

Unofficial fan project; not affiliated with PEAK or JoJo's Bizarre Adventure.
Built on BepInEx and More Customizations. No explicit reuse license is included;
please contact the maintainer about reusing project material.
