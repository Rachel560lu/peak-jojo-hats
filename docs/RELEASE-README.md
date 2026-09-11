![peak-jojo-hats](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/banner/peak-jojo-hats-header-v1.png)

# peak-jojo-hats

**JOJO's Bizarre Climb / JOJO 的奇妙登山**

JOJO-inspired hats and hairstyles for PEAK. 给 PEAK 小人换个 JOJO 发型。

Six head cosmetics inspired by Jotaro, Jolyne, Giorno, Josuke, Joseph and Jonathan, alongside your other cosmetics. **Version 0.5.2** updates the package cover; runtime logic is unchanged from v0.5.0 and the six models are unchanged from v0.4.2. The outfit concept preview remains below.

[In-game gallery and source](https://github.com/Rachel560lu/peak-jojo-hats) · [中文介绍](https://github.com/Rachel560lu/peak-jojo-hats/blob/main/README.zh-CN.md) · [Installation and troubleshooting](https://github.com/Rachel560lu/peak-jojo-hats/blob/main/docs/INSTALL.md) · [Report an issue](https://github.com/Rachel560lu/peak-jojo-hats/issues)

## In-game gallery / 实机展示

Here's how the six styles look in PEAK. Click a photo for the full-size image.

六款头饰的实机效果，点击照片可以查看原图。

| Jonathan Joestar · 乔纳森 | Joseph Joestar · 乔瑟夫 | Jotaro Kujo · 承太郎 |
| :---: | :---: | :---: |
| [![Jonathan's blue hairstyle in PEAK / 乔纳森蓝发实机展示](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/jonathan.png)](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/jonathan.png) | [![Joseph's brown hair and headband in PEAK / 乔瑟夫棕发与头带实机展示](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/joseph.png)](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/joseph.png) | [![Jotaro's black cap and hair in PEAK / 承太郎黑帽与头发实机展示](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/jotaro.png)](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/jotaro.png) |
| **Josuke Higashikata · 仗助** | **Giorno Giovanna · 乔鲁诺** | **Jolyne Cujoh · 徐伦** |
| [![Josuke's indigo pompadour in PEAK / 仗助牛排头实机展示](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/josuke.png)](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/josuke.png) | [![Giorno's golden rolls and braid in PEAK / 乔鲁诺金色三卷发实机展示](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/giorno.png)](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/giorno.png) | [![Jolyne's twin buns and lime bangs in PEAK / 徐伦双丸子与绿色刘海实机展示](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/jolyne.png)](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/images/jolyne.png) |

Only the hats and hair are included; the screenshots' eyes, outfits and props are not part of this mod. The models shown are unchanged in v0.5.0.

本模组只包含帽子和发型，不包含照片里的眼睛、服装和道具。v0.5.0 沿用图中的六款模型。

## Install

1. Install **JojoScoutHats v0.5.0 or newer** with r2modman or Thunderstore Mod Manager, including the dependencies.
2. Launch **modded PEAK** from the manager.
3. Open the passport's **Hat** tab and pick a JOJO icon.

**No scripts, file deletion or framework patches required.** Leave More Customizations and its included `built-in.pcab` as installed. Your other custom hats, eyes, faces and accessories stay in the catalog.

Dependencies: `BepInEx-BepInExPack_PEAK-5.4.75301` and `cretapark-More_Customizations-1.1.10`. The supported framework target is an unmodified 1.1.10 installation. For manual installation, copy the ZIP's `BepInEx/plugins/JojoHats` folder into your profile's `BepInEx/plugins` and keep its complete adjacent `assets` directory.

## Updating from v0.4.2

Equip a **vanilla hat** before updating and reselect your JOJO hat afterward; the old exclusive catalog and new shared catalog can use different positions.

Previously ran the JOJO-only script, patched More Customizations or removed its sample bundle? Start with a **fresh mod-manager profile**, or reinstall a clean copy of More Customizations 1.1.10 with its original DLL and `built-in.pcab`. v0.5.0 does not automatically change third-party files or restore old backups. **Do not rerun the old patch scripts.** See the installation guide for existing-profile recovery.

## Playing with friends

Share the **same complete cosmetic profile** with everyone in the lobby: JOJO, dependencies, all other cosmetic packs and their versions. Manually installed cosmetic files must match too. Matching only JOJO is not sufficient, and this mod does not send models to other players. Two-client appearance and reconnect validation are still pending; see [validation scope](https://github.com/Rachel560lu/peak-jojo-hats/blob/main/docs/VALIDATION.md).

## A few notes

- Only static headwear is included. The screenshots' eyes, outfits, expressions and props are not added by this mod.
- No added abilities or body replacements. Some outfits or climbing/ragdoll poses may still clip.
- Before disabling or removing the mod, equip a vanilla hat and close PEAK. Keep dependencies used by other mods. A normal v0.5.0 installation needs no framework repair afterward.

## 中文安装说明

包含乔纳森、乔瑟夫、承太郎、仗助、乔鲁诺和徐伦六款头饰，全部在护照的 **Hat / 帽子** 页选择。**v0.5.0** 改为与其他外观共存，六款模型沿用 v0.4.2。

1. 用 r2modman 或 Thunderstore Mod Manager 安装 **JojoScoutHats v0.5.0 或更新版本**，一并安装提示的依赖。
2. 从管理器启动 **Modded PEAK / 模组版游戏**。
3. 在护照的帽子页选择喜欢的 JOJO 图标。

**不需要运行脚本、删除文件或修改框架。** 保留 More Customizations 及其自带的 `built-in.pcab`。新版不隐藏其他自定义帽子、眼睛、表情或配件。依赖版本见上方；手动安装时保留 DLL 旁完整的 `assets` 目录。

### 旧版升级与联机

从 v0.4.2 升级前请换回原版帽子，升级后重新选择 JOJO 头饰，避免新旧列表位置变化造成选错。以前运行过 JOJO-only 补丁、修改过框架或删过样例包的话，最省心的方式是**新建管理器配置**；也可以重装包含原始 DLL 和样例包的 More Customizations 1.1.10。新版不自动修改其他模组或恢复旧备份，**不要再运行旧脚本**。

和朋友一起玩时，请使用**相同的完整外观配置**，依赖、其他外观包及其版本、手动安装的外观文件也要一致。本模组不自动传输模型，不能只保证 JOJO 版本相同。双客户端显示与重连验证仍待完成。

仅包含静态头饰，不包含展示图中的眼睛、衣服和道具。卸载前换回原版帽子并退出游戏，保留其他模组需要的依赖。正常安装的 v0.5.0 卸载后不需要修复框架；旧版修改过的配置需单独恢复。

[六款实机展示 / In-game gallery](https://github.com/Rachel560lu/peak-jojo-hats#in-game-gallery) · [详细安装与排错 / Full guide](https://github.com/Rachel560lu/peak-jojo-hats/blob/main/docs/INSTALL.md)

## Coming soon: JOJO outfits / 即将推出：JOJO 服装

Matching JOJO outfits for the six scouts are planned. Here's a first look at the idea.

计划给六位小人配上 JOJO 服装，先看看设计示意。

![JOJO outfits concept illustration / JOJO 服装设计示意图](https://raw.githubusercontent.com/Rachel560lu/peak-jojo-hats/main/docs/coming-soon/jojo-outfits-concept.png)

**Concept illustration, not an in-game screenshot.** These outfits are not included in the current hats mod. Final designs may change; no release date is set yet.

**这是概念示意图，不是实机截图。** 服装尚未包含在当前头饰模组中，最终造型可能调整，暂未确定发布日期。

## Credits / 致谢

Unofficial fan project; not affiliated with PEAK or JoJo's Bizarre Adventure. Built on BepInEx and More Customizations. No explicit reuse license is included; please contact the maintainer about reusing project material. The header is promotional artwork; gallery images are actual gameplay screenshots.

非官方同人项目，与 PEAK 或《JOJO 的奇妙冒险》官方无关联。感谢 BepInEx 和 More Customizations。项目未附带明确的再使用许可，如需使用素材请联系维护者。横幅为宣传插画，展示图为实机截图。
