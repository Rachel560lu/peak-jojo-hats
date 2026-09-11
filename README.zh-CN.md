<p align="center">
  <img src="docs/banner/peak-jojo-hats-header-v1.png" width="100%" alt="Six PEAK-style JOJO scouts surrounding the peak-jojo-hats title / 六位 PEAK 版 JOJO 围绕模组标题">
</p>

<h1 align="center">peak-jojo-hats</h1>

<p align="center">
  <strong>Six JoJos. One very bizarre climb.</strong><br>
  Six iconic hats and hairstyles for your next PEAK adventure.
</p>

<p align="center">
  <strong>六位 JOJO，一场奇妙登山。</strong><br>
  六款标志性帽子与发型，陪你攀登下一座 PEAK。
</p>

<p align="center">
  <a href="https://github.com/Rachel560lu/peak-jojo-hats/releases/latest"><img src="https://img.shields.io/badge/Download-GitHub_Releases-a4d56e?style=for-the-badge&amp;labelColor=555555" alt="Download on GitHub Releases / 在 GitHub 下载"></a>
  <a href="https://github.com/Rachel560lu/peak-jojo-hats/releases/tag/v0.4.2"><img src="https://img.shields.io/badge/Version-v0.4.2-405c68?style=for-the-badge&amp;labelColor=555555" alt="Version 0.4.2"></a>
  <a href="docs/INSTALL.md"><img src="https://img.shields.io/badge/BepInEx-5-405c68?style=for-the-badge&amp;labelColor=555555" alt="Requires BepInEx 5"></a>
  <img src="https://img.shields.io/badge/Hats-6-7560a8?style=for-the-badge&amp;labelColor=555555" alt="Six head cosmetics / 六款头饰">
</p>

<p align="center">
  <a href="https://github.com/Rachel560lu/peak-jojo-hats/releases/latest">Download / 下载</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.md">English</a> ·
  <a href="docs/INSTALL.md">Install / 安装</a> ·
  <a href="https://github.com/Rachel560lu/peak-jojo-hats/issues">Report an issue / 反馈</a>
</p>

为 **PEAK** 制作的非官方 JOJO 头饰模组。把六位主角的标志性发型与帽子带进游戏，以简洁配色、圆润体积和清晰轮廓融入小小侦察员的登山冒险。

> **只增加头饰。** 展示图里的眼睛、表情、服装和手持道具并非本模组新增。模组包含六款静态帽子栏外观，不增加技能、身体替换或头发物理。

## 实机展示

以下均为游戏截图，点击图片可查看原尺寸。

<table>
<tr><th>乔纳森·乔斯达</th><th>乔瑟夫·乔斯达</th><th>空条承太郎</th></tr>
<tr>
<td><a href="docs/images/jonathan.png"><img src="docs/images/jonathan.png" width="280" alt="乔纳森蓝色上扬发型的 PEAK 实机展示"></a></td>
<td><a href="docs/images/joseph.png"><img src="docs/images/joseph.png" width="280" alt="乔瑟夫棕色偏分与花纹发带的 PEAK 实机展示"></a></td>
<td><a href="docs/images/jotaro.png"><img src="docs/images/jotaro.png" width="280" alt="承太郎黑帽、金色徽章及帽下头发的 PEAK 实机展示"></a></td>
</tr>
<tr><th>东方仗助</th><th>乔鲁诺·乔巴拿</th><th>空条徐伦</th></tr>
<tr>
<td><a href="docs/images/josuke.png"><img src="docs/images/josuke.png" width="280" alt="仗助靛蓝牛排头的 PEAK 实机展示"></a></td>
<td><a href="docs/images/giorno.png"><img src="docs/images/giorno.png" width="280" alt="乔鲁诺金色三卷与后辫的 PEAK 实机展示"></a></td>
<td><a href="docs/images/jolyne.png"><img src="docs/images/jolyne.png" width="280" alt="徐伦深蓝双丸子、绿色刘海与辫子的 PEAK 实机展示"></a></td>
</tr>
</table>

## 包含内容

- 六款头饰：承太郎帽、仗助牛排头、乔鲁诺三卷、乔纳森蓝发、徐伦双丸子、乔瑟夫棕发。
- 连续发面、贴头发根与分区平滑法线，保留适合 PEAK 的简化风格。
- 可运行的 JSON 网格与可编辑 OBJ 模型。**游玩不需要安装 Blender 或 Unity Editor。**
- 通过 BepInEx 和 More Customizations 加载，在护照的帽子页选择。

## 安装

1. 在 r2modman 或 Thunderstore Mod Manager 中建立一个 **PEAK 专用配置**。
2. 安装测试过的依赖：`BepInEx-BepInExPack_PEAK-5.4.75301`、`cretapark-More_Customizations-1.1.10`。
3. 下载 [JojoScoutHats-0.4.2.zip](https://github.com/Rachel560lu/peak-jojo-hats/releases/download/v0.4.2/JojoScoutHats-0.4.2.zip)，作为本地模组导入；也可以把压缩包内的 `BepInEx/plugins/JojoHats` 文件夹复制到对应配置的 `BepInEx/plugins` 中。
4. 使用只有 JOJO、没有 `.pcab` 的配置时，先关闭游戏，按[详细安装说明](docs/INSTALL.md)运行随包附带的兼容脚本。它会备份并修改**本地** More Customizations DLL，再将自带样例包移出加载目录。
5. 从模组管理器启动游戏，进入护照的帽子页，翻到六款 JOJO 图标。

**不能只删除 `built-in.pcab`。** 未修改的 More Customizations 1.1.10 会拒绝空资源包列表；零资源包配置需要先完成兼容步骤。

## 兼容性与注意事项

- 本版会将**自定义外观目录**替换为六款 JOJO 头饰，其他自定义帽子、眼睛和配件不会显示；**原版外观仍可使用**。请勿直接装入混有其他外观包的常用配置。
- 联机玩家应安装一致的外观包和版本。本模组不会在玩家间传输模型文件，尚未完成双客户端联机验证。
- 卸载或切换回原版配置前，先换回一顶原版帽子。
- 依赖更新可能恢复样例包或改变兼容性。随包修复只在 More Customizations 1.1.10 上测试过。
- 所有头饰都是静态模型，尚未穷尽验证每套服装、第一人称镜头以及攀爬／布娃娃动作中的穿模情况。

## 开发与源码

当前版本：**0.4.2**。仓库包含 C# 加载器、程序化建模源码、JSON／OBJ 模型、共享色板以及六张原尺寸展示图。

参阅[构建与模型开发](docs/BUILD.md)、[验证范围](docs/VALIDATION.md)和[更新记录](CHANGELOG.md)。仓库不分发游戏程序集或其他模组 DLL；编译加载器需要你本地合法安装的 PEAK。

## 致谢与声明

顶部横幅为宣传插画；下方六张展示图均为真实游戏截图。

基于 [BepInEx](https://github.com/BepInEx/BepInEx) 和 [More Customizations](https://github.com/Creta5164/peak-more-customizations)。头部挂载参考了其[帽子制作指南](https://github.com/Creta5164/peak-more-customizations/blob/main/docs/hat.md)。

这是非官方同人项目，与 PEAK 或《JOJO 的奇妙冒险》的创作者及权利方没有隶属或背书关系。模组网格为本项目制作；截图包含游戏及其原有外观。仓库目前未附加明确的再使用许可，如需复用请先联系维护者。
