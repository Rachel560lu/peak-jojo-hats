# Validation scope / 验证范围

This page separates current runtime checks, historical model evidence and untested behavior. A successful build or smoke test is **not** proof that every game version, cosmetic combination or multiplayer lobby works.

## v0.5.0 release checks

The runtime now appends six JOJO hats to the framework catalog and uses an **unmodified More Customizations 1.1.10** installation with its included `built-in.pcab`. The old zero-bundle, exclusive-catalog smoke test below is not evidence for this new installation path.

| Check | Current status / required evidence |
|---|---|
| Release build | **PASS.** .NET SDK 8.0.424, Release, zero warnings/errors; Unity 6000.3.15f1, BepInExPack_PEAK 5.4.75301, original More Customizations 1.1.10. |
| Asset validation | **PASS.** All six models, OBJ parity, normals, palette coordinates and icons; unchanged v0.4.2 model revision. |
| Catalog unit tests | **22/22 PASS.** Reference/order preservation, atomic failure, duplicate registration, collisions, category independence and read-only publication. |
| Package validation | **PASS.** 19 ZIP entries; 256 x 256 PNG icon; own DLL/assets and metadata only. No scripts, test DLL, third-party DLLs or `.pcab` files. |
| Clean package-based install | **PASS.** Fresh official dependency ZIPs plus release ZIP in manager-style folders, no patch scripts. 7 custom hats (1 framework + 6 JOJO), 5 existing non-hat cosmetics preserved. Not a mod-manager UI test. |
| Catalog coexistence | **PASS with Umamusume Hats 0.1.1.** 42 custom hats (35 Umamusume + 1 framework + 6 JOJO), 5 existing non-hat cosmetics. Existing entry references and order, character attachments, isolated passport icons/names verified. Other packs are not exhaustively tested. |
| Restart | **PASS.** Two consecutive launches in both clean and mixed profiles; fresh results, six JOJO hats without duplication, dependency and other-pack file hashes unchanged. |
| Missing own resources | **PASS.** Removed the JOJO Joseph mesh, then separately a Jolyne icon, in disposable profiles. Each failure left all 36 foreign hats and 5 non-hat cosmetics intact, with zero partially registered JOJO hats. |
| Saved selection / real passport UI | **Not yet validated.** Isolated passport registration is not actual menu navigation, save persistence or reselection. No save or Steam-stat migration was attempted. |
| Upgrade | **PASS for old-binary replacement with pristine dependencies.** Actual v0.4.2 DLL then v0.5.0: 6 exclusive hats become 42 shared hats; 5 non-hat entries restored. Previously patched framework profiles and old saved selections are not automatically repaired or verified. |
| Disable/uninstall | **PASS for removing the plugin folder.** Foreign catalog returns to its baseline and dependency hashes stay unchanged. Manager-specific disable UI and saved selection were not exercised; equip a vanilla hat first. |
| Mod-manager UI install | Pending a fresh profile installed through the manager's actual download/install/launch flow. |
| Two-client multiplayer | **Not yet validated.** Both clients must use the same complete cosmetic profile; check appearance, rejoin and reconnect. |

Checks were run on Windows on **2026-09-12**. The tested Release DLL SHA-256 is `89DADE44ABBFB31B0D1C707988FEDE829BE369A4E632BD5A422688C7D06B1808`. The own-content fingerprint is `2fa0cbcf69d986146e42d83572f975b83bf9ea047ccee769864652ecf83dee0b`; this is not a hash of the full cosmetic profile and cannot prove multiplayer compatibility.

The runtime tests use fresh isolated profiles and real Unity/More Customizations code with `-batchmode -nographics`. They do not create a lobby or change the player's saved hat. Each launch requires a newly written result and successful process exit; stale results cannot count as passes. The test-only passport/character clones restore the framework counters and material/shader caches and clean up test-owned objects.

The optional local game serialization check could not run at batch startup because the real passport singleton was not initialized. Ordinary smoke results explicitly record `localGameSerializationRoundTrip=NOT_RUN` and `twoClientMultiplayer=NOT_TESTED`. Do not interpret catalog tests as network tests.

The test environment also emitted BepInEx/Unity logging interop warnings and game-service authentication/no-graphics warnings. Mod-specific checks completed, but these are **not error-free interactive or online sessions**. Raw logs, personal paths, player identifiers, local profiles and third-party assemblies are intentionally not published.

## Existing model and source evidence (v0.4.2)

- The v0.4.2 portable C# Release build passed with .NET SDK **8.0.424**, zero warnings and zero errors, using local PEAK and More Customizations 1.1.10 references. This is a historical result, not the v0.5.0 build result.
- `tools/validate_assets.py` checks all six JSON/OBJ exports: finite coordinates, index ranges, nondegenerate triangles, unit normals, palette UVs, matching metadata, icon dimensions and OBJ coordinate parity.
- The catalog totals **81,256 triangles / 42,146 vertices** across six hats. Only the selected hat is worn; these totals are not a frame-time benchmark.
- Josuke's connected surface, head clearance and intended hairline opening are checked. Josuke, Jolyne and the palette are protected by frozen SHA-256 hashes.
- The stored v0.4.2 generation reports record 2,522 preserved Jotaro cap triangles and at least 7,384 preserved Giorno signature triangles. The validator checks these reports; rerunning the exporter recomputes the geometry comparisons.
- GitHub Actions is configured to run the **asset validator and catalog unit tests**, not PEAK or the plugin build. Game/dependency assemblies are deliberately absent from this public repository.

## Historical runtime and visual evidence

The v0.4.2 development build passed a Unity **6000.3.15f1** no-graphics smoke test in an isolated, patched profile: six custom hats, zero custom non-hat entries, zero `.pcab` bundles, and passing mesh/normal and menu icon ordering checks. That setup has been **retired for normal v0.5.0 installations** and does not test mixed cosmetics or clean dependency loading. It was not an interactive end-to-end UI test.

The six [gallery images](../README.md#in-game-gallery) are actual gameplay screenshots supplied during visual testing of the unchanged model revision, not offline concept renders. They are evidence of model appearance, not the new registration, install, upgrade or multiplayer behavior.

## Remaining limits

- Two-client appearance, cosmetic ordering and reconnect behavior require real multiplayer validation. Models are not automatically transferred to players; use identical complete cosmetic profiles, including manually installed files.
- Not all first-person views, outfits, climbing and ragdoll poses have been checked for clipping.
- Future PEAK/More Customizations versions and non-Windows installations are not guaranteed.
- No large-player-count GPU/CPU performance benchmark is claimed.
- These are static meshes; lack of braid or strand motion is intentional.

## 中文摘要

v0.5.0 改为在原有外观列表后添加六款头饰，正常安装使用未修改的 More Customizations 1.1.10 和自带样例包。构建、六款资源验证和 22 项目录回归检查已通过；从发布 ZIP 组装的干净环境及 Umamusume 混装环境均通过两次启动。混装后保留 35 款 Umamusume 头饰、1 款框架帽子和 5 项非帽子外观，另外添加 6 款 JOJO。依赖文件哈希未变。单独移走 JOJO 模型或图标的失败测试也通过：其他外观保持完整，不会加载半套 JOJO。

旧版 DLL 升级和移除本模组后的外观目录检查已通过，但不代表自动修复旧版改过的框架或迁移旧存档选择。管理器界面完整点击安装、真实护照选帽保存、双客户端联机与重连仍**未验证**。无图形启动时没有真实护照单例，因此本地游戏序列化检查也未计为通过。测试存在框架日志互操作及游戏服务认证警告，不能宣称是无错误的在线实测。

v0.4.2 的实机展示图和旧版零资源包冒烟测试仅是历史证据，不能代替新版完整玩家流程的验证。模型保持不变。自动化 CI 配置为检查**模型资源和目录单元测试**，不启动游戏。

双客户端联机显示与重连仍待验证，玩家需使用相同的完整外观配置。所有动作与服装穿模、未来版本、非 Windows 环境和大规模性能也尚未全面验证。
