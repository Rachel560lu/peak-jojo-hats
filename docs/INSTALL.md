# Installation / 安装说明

[English README](../README.md) · [中文介绍](../README.zh-CN.md) · [Download](https://github.com/Rachel560lu/peak-jojo-hats/releases/latest)

## Before you start

Use a **dedicated PEAK mod profile**. This version replaces the framework's entire
**custom** cosmetic catalog with six JOJO hats, not just its Hat category. Other
custom eyes, faces, hats and accessories will not be listed. Vanilla cosmetics
remain available. The screenshots' outfits, eyes, expressions and props are not
part of this package.

Tested dependencies:

- `BepInEx-BepInExPack_PEAK-5.4.75301`
- `cretapark-More_Customizations-1.1.10`

The mod uses JSON meshes rather than `.pcab` bundles. Unmodified More
Customizations 1.1.10 throws when no bundles exist, so **deleting `built-in.pcab`
alone is not enough**. The included compatibility script patches that local
framework check. No patched third-party DLL is distributed.

## Install on Windows

1. Create a PEAK profile in your mod manager and install the dependencies above.
2. Download the release's **JojoScoutHats-0.4.2.zip** asset (not GitHub's automatic
   Source code ZIP). Close PEAK before changing the profile.
3. Extract the ZIP to a temporary folder. Copy `BepInEx/plugins/JojoHats` into the
   profile's `BepInEx/plugins` directory, preserving the `assets` folder beside
   `JojoHats.dll`. If you use your manager's local-mod import, still extract the
   ZIP separately to access the compatibility scripts.
4. Find the profile's actual `BepInEx` directory using the mod manager's profile
   folder command. From the **extracted ZIP root**, open PowerShell and run the
   following, replacing the placeholder with that full path:

   ```powershell
   .\scripts\install-jojo-only.ps1 -BepInExRoot 'FULL_PATH_TO_PROFILE\BepInEx'
   ```

5. The script requires exactly one `MoreCustomizations.dll`. It backs the original
   up to `BepInEx/JojoHats-backup/MoreCustomizations.original.dll`, patches the
   installed copy, and moves the adjacent `built-in.pcab` into a timestamped file
   in the same backup directory. **Do not move that backup under `plugins`.**
6. Start **modded** PEAK using this profile. Open the passport's Hat tab and page
   through the custom entries to find the six JOJO icons.

Review the scripts before running them. They act on the profile path you supply;
they do not install dependencies or copy the JOJO plugin automatically. A normal
user-owned mod-manager profile should not need administrator privileges.

### Updating dependencies

The patch has been tested only with More Customizations **1.1.10**. Its guard
checks the loader's instruction pattern, not an explicit version allowlist.
Do not assume it supports a newer framework just because the script runs.

Updating/reinstalling More Customizations may restore its sample or replace the
patched DLL. The installer reuses an existing original-DLL backup, so **do not
rerun it across a framework-version change**: use a fresh dedicated profile with
the tested dependencies. Preserve the old backup for recovery.

## Troubleshooting

| Symptom | Check |
|---|---|
| `No customization files found` | Run the compatibility step with PEAK closed; merely removing the sample bundle does not patch the loader. |
| No JOJO icons | Confirm modded launch, both dependencies, and `JojoHats.dll` with its complete adjacent `assets` folder. |
| Other custom cosmetics disappeared | Expected in this JOJO-only profile. Use a separate profile for mixed cosmetic packs. |
| Script reports unsupported/unknown framework | Stop; do not bypass the guard. Use an untouched copy of the tested framework in a fresh profile. |
| Script cannot find exactly one framework DLL | Check that the supplied directory is the intended profile's `BepInEx`, and that it has no duplicate framework installations. |

For bug reports, include PEAK/mod/dependency versions, the affected hat and angle,
and a screenshot. Share only relevant log excerpts after removing personal paths,
player identifiers and lobby details. [Report an issue](https://github.com/Rachel560lu/peak-jojo-hats/issues).

## Multiplayer and removal

Use matching mod/dependency versions on every participating client. Mesh files
are **not** sent over the network, and two-client behavior has not yet been
validated. See [validation scope](VALIDATION.md).

Before uninstalling, equip a vanilla hat and close PEAK. Disable/remove this
profile's `JojoHats` folder. To restore the framework, replace its modified DLL
with the saved original from this same installation (or reinstall the tested
framework); restore the saved sample to the framework folder as `built-in.pcab`
if desired. Do not restore a backup from a different dependency version.

## 中文快速说明

1. 建议新建 **JOJO 专用 PEAK 配置**，安装上面列出的两个测试版本依赖。
2. 下载 Release 中的 `JojoScoutHats-0.4.2.zip`，不要下载自动生成的 Source code 包。
3. 关闭游戏，解压并将 `BepInEx/plugins/JojoHats` 复制到该配置的 `BepInEx/plugins`。
   必须保留 DLL 旁完整的 `assets` 文件夹。通过本地模组导入安装时，也要另外解压以运行脚本。
4. 在解压目录打开 PowerShell，运行上面的安装命令，将占位路径换成该配置的真实 `BepInEx` 路径。
5. 脚本先备份原版框架 DLL，再修改本地空资源包检查，并把 `built-in.pcab` 移到
   `BepInEx/JojoHats-backup`。备份可以恢复，不要把它放回 `plugins` 子目录。
6. 从模组管理器启动游戏，在护照的帽子页找到六款 JOJO 图标。

只删除 `built-in.pcab` 会导致未修复的 1.1.10 框架报错。本模组只提供头饰，不提供截图里的
眼睛、服装或道具；它会隐藏**其他自定义外观**，但保留原版外观。

兼容修复只测试过 1.1.10，并非通用版本补丁。框架更新会改变本地状态；脚本会复用旧备份，
因此跨框架版本时不要直接重跑，请用包含测试版本依赖的新配置。卸载前换回原版帽子并关闭游戏，
再移除 JOJO 文件夹，按需恢复同一版本的框架 DLL 和样例包。联机双客户端验证仍待完成。
