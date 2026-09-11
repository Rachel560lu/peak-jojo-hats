# Installation / 安装说明

[English README](../README.md) · [中文介绍](../README.zh-CN.md) · [Thunderstore download / 下载](https://thunderstore.io/c/peak/p/Rachel560lu/JojoScoutHats/)

These instructions apply to **v0.5.0 and newer**, using unmodified More Customizations **1.1.10**. For v0.4.2 profiles, read the upgrade section below first.

## Install with a mod manager

1. In r2modman or Thunderstore Mod Manager, select **PEAK** and install [Rachel560lu / JojoScoutHats](https://thunderstore.io/c/peak/p/Rachel560lu/JojoScoutHats/), version **0.5.0 or newer**, with its dependencies.
2. Start **modded PEAK** from the manager.
3. Open the passport's **Hat** tab and select one of the six JOJO icons.

That's all for a normal installation. **No scripts, file deletion or framework patches are required.** Leave More Customizations and its included `built-in.pcab` as installed. This mod adds hats to the existing catalog; it does not remove your other custom eyes, faces, hats or accessories.

Declared dependencies:

- `BepInEx-BepInExPack_PEAK-5.4.75301`
- `cretapark-More_Customizations-1.1.10`

The six hairstyles all use the Hat slot. Screenshot outfits, eyes, expressions and props are not included.

## Playing with friends

Share your mod manager's profile code or profile export, then have everyone use the **same complete cosmetic profile**: JOJO, More Customizations, all other cosmetic packs and their versions. If you manually added cosmetic files, make sure those files match too; do not assume a profile code includes them.

Matching only the JOJO version is not sufficient. Cosmetic ordering is handled by the framework, and this mod does **not** transfer model files to other players. Two-client appearance and reconnect validation are still pending; see [validation scope](VALIDATION.md). A different/missing cosmetic profile is not a supported multiplayer setup.

## Upgrading from v0.4.2

1. Before changing versions, equip a **vanilla hat** and close PEAK. Back up or duplicate the old profile if you want to keep it.
2. If you previously ran `install-jojo-only.ps1`, removed `built-in.pcab` or manually patched More Customizations, the simplest route is a **fresh mod-manager profile**. Install the dependencies and v0.5.0 normally there.
3. If the old profile's dependencies are untouched, update JojoScoutHats through the manager. Keep only one installed copy of `JojoHats.dll`.
4. Launch modded PEAK and reselect your JOJO hat. The old exclusive catalog and new shared catalog can have different positions.

v0.5.0 does not inspect, overwrite or restore your old backups. It also does not modify the framework DLL or move bundles. A new plugin cannot automatically undo a patch previously made to another mod.

To repair an existing modified profile instead of starting fresh, close the game and **reinstall a clean copy of More Customizations 1.1.10**, including its original DLL and `built-in.pcab`. Advanced users can restore a known original backup from the **same framework version and installation**. Do not overwrite a newer framework with an old backup or place backup DLLs under `plugins`. Keep the old backup until you have checked the repaired profile. The historical patch scripts remain in the source repository only; do not rerun them for v0.5.0.

## Manual installation

Close PEAK. Install the two dependencies first, then download the **v0.5.0 or newer package ZIP** from Thunderstore (not GitHub's automatic Source code ZIP). Extract it and copy `BepInEx/plugins/JojoHats` into your profile's `BepInEx/plugins` folder.

Keep `JojoHats.dll` and the complete adjacent `assets` directory together. On updates, replace this mod's own folder rather than keeping an old copy beside it. Do not copy game DLLs or another profile's framework files. Launch through your mod manager or an already configured BepInEx installation.

## Troubleshooting

| Symptom | What to check |
|---|---|
| No JOJO icons | Confirm you launched modded PEAK, installed both dependencies and kept the complete `assets` folder beside `JojoHats.dll`. Check the remaining pages of the Hat tab. |
| `No customization files found` | The framework's sample may have been removed by an older setup. Start with a fresh profile or reinstall clean More Customizations 1.1.10, including `built-in.pcab`. Do not apply the old empty-bundle patch. |
| Other custom cosmetics disappeared | Check you are running v0.5.0 or newer and have no old JOJO DLL left in the profile. The new version does not intentionally hide other packs. |
| The wrong hat is selected after updating | Switch to a vanilla hat, then select the desired JOJO icon again; the shared catalog can use different positions. |
| Friends see different cosmetics | Compare the complete cosmetic profiles, not just JOJO. Match dependency versions, other cosmetic packs and manually installed cosmetic files; restart after changes. |
| A dependency update breaks loading | The supported target is unmodified More Customizations 1.1.10. Reproduce in a fresh profile with the declared versions and report the error; do not patch or downgrade an unrelated working profile blindly. |

For a bug report, include PEAK/mod/dependency versions, other cosmetic packs, the affected hat and a screenshot. Share relevant log excerpts only, with personal paths, player identifiers and lobby details removed. [Report an issue](https://github.com/Rachel560lu/peak-jojo-hats/issues).

## Disabling or removing

Equip a **vanilla hat**, close PEAK, then disable or uninstall JojoScoutHats in the mod manager. Keep shared dependencies if other mods use them. A normal v0.5.0 install leaves no third-party DLL patch or moved bundle to undo. Profiles previously modified by v0.4.2 still need the separate recovery described above.

## 中文安装说明

以下适用于 **v0.5.0 及更新版本**，适配未修改的 More Customizations **1.1.10**。

1. 在 r2modman 或 Thunderstore Mod Manager 选择 **PEAK**，安装 [Rachel560lu / JojoScoutHats](https://thunderstore.io/c/peak/p/Rachel560lu/JojoScoutHats/) **0.5.0 或更新版本**，一并安装提示的依赖。
2. 从管理器启动 **Modded PEAK / 模组版游戏**。
3. 在护照的 **Hat / 帽子** 页选择喜欢的 JOJO 图标。

正常安装**不需要运行脚本、删除文件或修改框架**。保留依赖及其自带的 `built-in.pcab` 即可。新版只增加六款头饰，不隐藏其他自定义帽子、眼睛、表情和配件；截图中的服装与道具不属于本模组。

### 和朋友一起玩

请通过管理器分享配置代码或导出配置，让每个人使用**相同的完整外观配置**，包括 JOJO、框架、其他外观包及其版本。手动添加的外观文件也要保持一致，不能默认配置代码一定包含这些文件。只装同一个 JOJO 版本还不够。

本模组不会自动传输模型，外观顺序由框架管理。双客户端显示与重连验证仍待完成，不支持外观包不一致的联机配置。

### 从 v0.4.2 升级

升级前换回**原版帽子**并关闭游戏，按需备份旧配置。若以前运行过 JOJO-only 脚本、修改过框架或删过样例包，最省心的方式是**新建一个管理器配置**，重新安装依赖和新版 JOJO。

依赖从未修改过的配置可以直接更新；确保只留下一个 JOJO DLL，进入游戏后重新选择头饰。旧版独占列表和新版共存列表中的位置可能不同。新版不会自动恢复旧备份或修改其他模组的文件，也**不要再运行旧脚本**。

想保留旧配置时，先关闭游戏，再重新安装干净的 More Customizations 1.1.10，恢复其原始 DLL 和 `built-in.pcab`。熟悉文件操作的用户也可以恢复**同一框架版本、同一安装**的原始备份，但不要用旧备份覆盖新版框架，也不要把备份 DLL 放进 `plugins`。确认恢复正常前请保留备份。

### 手动安装、排错与卸载

手动安装时先装好两个依赖，下载 Thunderstore 的模组 ZIP，将 `BepInEx/plugins/JojoHats` 复制到对应配置；保留 DLL 旁完整的 `assets` 目录。不要下载 GitHub 自动生成的 Source code 包来直接安装。更新时替换本模组自己的文件夹，别让新旧 DLL 同时存在。

- **没有 JOJO 图标**：确认启动了模组版游戏、依赖齐全、资源目录完整，再翻一下帽子页。
- **提示找不到 customization files**：旧配置可能移除了样例包，请新建配置或重装干净的框架，不要套用旧补丁。
- **其他外观消失**：确认安装的是 v0.5.0 或更新版本，且没有旧 JOJO DLL 残留。
- **升级后选错帽子**：先选原版帽子，再选一次想要的 JOJO 头饰。
- **队友看到不同外观**：核对所有外观包、依赖和手动文件，修改后重新启动游戏。

卸载前换回原版帽子并退出游戏，再从管理器禁用或卸载 JOJO；其他模组仍使用的依赖请保留。正常安装的 v0.5.0 没有框架补丁或移动过的样例需要恢复，旧版修改过的配置除外。反馈时请附版本、其他外观包和截图，日志中请先去掉个人路径及房间信息。
