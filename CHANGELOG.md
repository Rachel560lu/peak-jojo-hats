# 0.5.2

- Update the package cover with the revised, borderless JOJO scout illustration.
- No changes to models, cosmetic IDs, dependencies or runtime logic.

中文：更新为无边框新版封面，六款头饰与加载逻辑不变。

# 0.5.1

- Add a bilingual coming-soon section and concept illustration for planned JOJO outfits.
- Clearly distinguish the concept from the in-game gallery: outfits are not included, and no release date is set.
- No changes to hat models, cosmetic IDs, dependencies or runtime logic; only release version metadata changes in the loader.

中文：新增 JOJO 服装预告与设计示意图，明确服装尚未包含、暂无发布日期。六款头饰与加载逻辑不变。

# 0.5.0

- Add six JOJO hats alongside the existing cosmetic catalog instead of replacing it; keep other custom hats, eyes, faces and accessories.
- Use unmodified More Customizations 1.1.10 with its included sample bundle. Normal installs no longer require PowerShell or third-party DLL patches.
- Remove the historical JOJO-only installer and empty-bundle patch scripts from the download package. Existing profile files and backups are not changed automatically.
- Add mod-manager installation, v0.4.2 migration, removal and matching-profile multiplayer instructions in English and Chinese.
- Include the six-image in-game gallery directly in the Thunderstore description, with bilingual captions and full-size image links.
- Keep the six models, textures and cosmetic IDs from v0.4.2. Asset revision numbers remain independent of the loader version.
- Multiplayer appearance and reconnect behavior still require two-client validation; no automatic asset synchronization is provided.

中文：现在只添加六款头饰，不隐藏其他自定义外观；正常安装不再需要脚本或修改框架。模型不变。旧版修改过依赖的配置建议重新建立，联机请使用相同的完整外观配置。

# 0.4.2

- Extend continuous-volume / fitted-root refinement to Jotaro, Jonathan and Joseph.
- Conservative Giorno cleanup: one scalp envelope and continuous spiral ridges; accepted locks, roll bodies and braid positions preserved.
- Josuke/Jolyne and shared palette remain byte-identical to v0.4.1.
- Same six IDs, hat order and runtime architecture; no added eyes, clothing, textures or PCAB content.
- Per-hat exported-mesh comparisons, six-view sheets and 12-angle turntables.

# 0.4.1

- Targeted Josuke/Jolyne refinement from gameplay feedback; other four hats and palette frozen byte-for-byte.
- One continuous Josuke forehead-roll/crown/scalp surface, shallow integrated ridges, no detached top tufts.
- Jolyne gathered green roots and continuous braid follow the curved skull; tapered tie and smaller tail.
- Same runtime architecture, custom catalog, material, IDs and hat order.
- Real-mesh before/after comparison, six-views and regression checks; no visual gameplay approval implied.

# 0.4.0

- Six character-specific layouts replacing the generic rear-hair template.
- Surface-following tapered locks with independently controlled width and thickness.
- Stable transported sweep frames and part-local authored smooth normals.
- Indexed runtime mesh and normal-aware CPU previews.
- Revised Jotaro cap opening, full band, visor and hidden hair roots.
- Filled Josuke pompadour, swept Giorno crown, raised Jonathan fan, asymmetrical Joseph crown.
- Interwoven Jolyne bun rings, shallow pulled-back hair and continuous braid strands.
- All six use the shared palette; no separate high-resolution texture dependency.
- Per-hat six-view sheets, 12-angle turntables and expanded normals validation.
- Replaced the previous layered rear-hair construction.

# 0.2.0

- Rebuilt all six models from the approved six-view designs with curved faceted locks.
- Navy Jolyne buns, lime braided bases/bangs/back braid, teal tie; no all-green buns.
- Asymmetric Jotaro crown, solid gold cord and raised hand badge; removed coat chain.
- Rolled indigo Josuke perimeter and interwoven top/back; no waffle slab.
- Solid Giorno spiral rolls and rear braid; blue-violet Jonathan fan/forelocks; Joseph patterned headband.
- JOJO-only custom catalog: six hats, zero custom eyes, faces or accessories; vanilla preserved.
- Recoverable sample removal and narrow offline empty-bundle framework compatibility fix.
- Actual-mesh six-view exports, expanded validation and zero-pcab runtime assertions.

# 0.1.0

- Initial six static low-poly hats, including corrected compact Josuke pompadour.
- Shared texture atlas, six passport icons, deterministic mesh source and OBJ exports.
- Runtime registration through More Customizations 1.1.10.
- Isolated PEAK smoke-test workflow.
