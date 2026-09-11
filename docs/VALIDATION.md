# Validation scope

This page separates automated checks from visual evidence and untested behavior.
The project is a six-hat cosmetic MVP, not a claim of compatibility with every
PEAK update or mod combination.

## Public source and assets

- The portable C# Release build passed with .NET SDK **8.0.424**, zero warnings
  and zero errors, using local PEAK and More Customizations 1.1.10 references.
- `tools/validate_assets.py` checks all six JSON/OBJ exports: finite coordinates,
  index ranges, nondegenerate triangles, unit normals, palette UVs, matching
  metadata, icon dimensions and OBJ coordinate parity.
- The catalog totals **81,256 triangles / 42,146 vertices** across six hats.
  Only the selected hat is worn; these totals are not a frame-time benchmark.
- Josuke's connected surface, head clearance and intended hairline opening are
  checked. Josuke, Jolyne and the palette are protected by frozen SHA-256 hashes.
- The stored v0.4.2 generation reports record 2,522 preserved Jotaro cap triangles
  and at least 7,384 preserved Giorno signature triangles. The validator checks
  these reports; rerunning the exporter also recomputes the geometry comparisons.
- GitHub Actions runs the **asset validator**, not PEAK or the plugin build.
  Game/dependency assemblies are deliberately absent from this public repository.

## Runtime and visual evidence

The development build passed a Unity **6000.3.15f1** no-graphics smoke test in a
dedicated profile: six custom hats registered, zero custom non-hat entries,
zero `.pcab` bundles, mesh/normal checks and menu icon ordering passed.
The smoke fixture is not an interactive end-to-end UI test.

The six images in [the gallery](../README.md#in-game-gallery) are actual gameplay
screenshots supplied during visual testing of this model revision. They show
the head cosmetics on PEAK characters, not offline concept renders. The public
loader was rebuilt for portable paths and clean release symbols; that newly
compiled binary has not had a separate in-game test in the publication step.

Raw game logs, local test profiles and third-party assemblies are not published.

## Still to verify

- Two-client multiplayer appearance, synchronization and reconnect behavior.
- All first-person views, outfits, climbing and ragdoll poses for clipping.
- Mixed custom-cosmetic packs (this release intentionally takes over the custom
  catalog and is intended for a dedicated profile).
- Future PEAK/More Customizations versions and non-Windows installations.
- Performance at large player counts; no formal GPU/CPU benchmark is claimed.

The hats are static meshes; lack of braid or strand motion is intentional.

## 中文摘要

公开源码编译通过，六款网格有自动检查和实机展示图。自动化 CI **只验证模型资源**，不会启动游戏。
开发版完成了零资源包运行时冒烟检查，但发布时重新编译的 DLL 没有额外重跑局内测试。
双客户端联机、所有动作和服装的穿模、未来版本兼容性与性能基准仍未全面验证。
