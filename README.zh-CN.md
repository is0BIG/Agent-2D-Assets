# Agent-2D-Assets

语言：[English](./README.md) | [繁体中文](./README.zh-TW.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md)

<p align="center">
  <img src="./src/banner.png" alt="Agent-2D-Assets banner" width="900" />
</p>

<p align="center">
  <strong>面向 Codex 的 2D 游戏资产工作流：生成可用于 Godot、Unity 或原生 2D 项目的角色、地图和音频素材。</strong>
</p>

<p align="center">
  用自然语言描述需求。Codex 负责资产规划与生成，本地脚本负责去背、切帧、对齐、质量检查、音频处理和导出。
</p>

<p align="center">
  <a href="#项目特点">项目特点</a> |
  <a href="#包含的-skills">Skills</a> |
  <a href="#godot-可用性">Godot</a> |
  <a href="#安装">安装</a> |
  <a href="#示例提示词">提示词</a> |
  <a href="#示例音频素材">音频素材</a>
</p>

## 项目特点

Agent-2D-Assets 不是单纯的提示词合集，而是一套 Codex-first 的 2D 游戏资产流水线：

1. Codex 根据需求判断资产类型、风格、视角、输出格式和引擎目标。
2. 视觉资产由图像生成或用户提供的素材产生。
3. 本地 Python 脚本完成可重复的清理、切帧、对齐、分析和导出。
4. 输出素材带有元数据，方便继续接入 Godot、Unity、Web 或其他 2D 游戏项目。

当前已经包含三类核心资产：

| 类型 | Skill | 适合生成 |
| --- | --- | --- |
| 角色与特效 | [`generate2dsprite`](./skills/generate2dsprite) | 角色、怪物、NPC、道具、法术、投射物、命中特效、动画帧 |
| 地图与场景 | [`generate2dmap`](./skills/generate2dmap) | RPG 地图、分层场景、TileMap、碰撞、区域、出口、Godot 场景草案 |
| 音频与音效 | [`generate2daudio`](./skills/generate2daudio) | UI 音效、战斗音效、法术音效包、循环音、WAV 分析和 manifest |

## Godot 可用性

这三个 skill 生成的内容都可以用于 Godot，但接入方式略有不同。

| Skill | Godot 用法 | 输出内容 |
| --- | --- | --- |
| `$generate2dsprite` | 透明 PNG、sprite sheet、frame PNG 可导入 `Sprite2D`、`AnimatedSprite2D`、`SpriteFrames` 或 `AnimationPlayer` | `sheet-transparent.png`、frame PNG、GIF 预览、`pipeline-meta.json` |
| `$generate2dmap` | 可用于 `TileMapLayer`、`Sprite2D` props、`Area2D` 区域、`StaticBody2D` 碰撞和场景 metadata | base map、prop pack、placements、collision、zones、preview、Godot scene 草案 |
| `$generate2daudio` | WAV 可直接导入 Godot 作为 `AudioStreamWAV`，用于 `AudioStreamPlayer` 或 `AudioStreamPlayer2D` | WAV、单文件分析 JSON、`audio-pack.json`、目录分析报告 |

建议的 Godot 工作流：

```text
$generate2dsprite -> 角色 / 敌人 / FX
$generate2dmap    -> 地图 / 碰撞 / 出生点 / 出口
$generate2daudio  -> UI / 战斗 / 法术 / 环境音
Godot             -> 组装成场景、节点、脚本和可运行 demo
```

## Showcase

### Godot 可编辑地图

`$generate2dmap` 可以输出面向 Godot 的可编辑地图结构，而不只是单张扁平图片。

<p align="center">
  <img src="./src/godot-editor.png" alt="Generate2DMap Godot editor scene" width="860" />
  <br />
  <strong>Godot editor scene：TileMapLayer、独立 props、区域、碰撞、出口和 debug player</strong>
</p>

Godot 地图输出可以包含：

- 可编辑 `TileMapLayer`
- 独立 `Sprite2D` props
- `Area2D` 触发区、遇敌草丛和出口
- `StaticBody2D` 碰撞阻挡
- 玩家出生点、相机、debug player
- 结构化 placement / collision / zones metadata

### Sprite Sheets And FX

`$generate2dsprite` 适合生成动画角色、怪物、法术、投射物和命中特效。

<table>
  <tr>
    <td align="center" width="25%">
      <img src="./src/goku-kame.gif" alt="Goku Kamehameha sprite animation" width="170" />
      <br />
      <strong>Attack animation</strong>
    </td>
    <td align="center" width="25%">
      <img src="./src/naruto-rasengan.gif" alt="Naruto Rasengan sprite animation" width="170" />
      <br />
      <strong>Character action</strong>
    </td>
    <td align="center" width="25%">
      <img src="./src/cast.gif" alt="Fire mage cast animation" width="150" />
      <br />
      <strong>Spell cast</strong>
    </td>
    <td align="center" width="25%">
      <img src="./src/projectile.gif" alt="Fire mage projectile animation" width="150" />
      <br />
      <strong>Projectile</strong>
    </td>
  </tr>
</table>

### 分层地图流程

`$generate2dmap` 适合做 clean HD RPG map、分层场景、prop pack 和碰撞数据。

<table>
  <tr>
    <td align="center" width="33%">
      <img src="./src/cyber-canal-base.png" alt="Ground-only cyberpunk canal RPG base map" width="300" />
      <br />
      <strong>Ground-only base</strong>
    </td>
    <td align="center" width="33%">
      <img src="./src/cyber-canal-dressed-reference.png" alt="Dressed cyberpunk canal reference map" width="300" />
      <br />
      <strong>Dressed reference</strong>
    </td>
    <td align="center" width="33%">
      <img src="./src/cyber-canal-prop-pack.png" alt="Generated 3x3 cyberpunk canal prop pack" width="300" />
      <br />
      <strong>3x3 prop pack</strong>
    </td>
  </tr>
</table>

<p align="center">
  <img src="./src/cyber-canal-layered-preview.png" alt="Layered cyberpunk canal RPG map preview" width="760" />
  <br />
  <strong>Flattened layered RPG map preview</strong>
</p>

## 包含的 Skills

### `$generate2dsprite`

用于生成和处理独立 2D sprite 资产。

常见输出：

- `raw-sheet.png`
- `raw-sheet-clean.png`
- `sheet-transparent.png`
- frame PNGs
- `animation.gif`
- 可选 APNG / WebP 预览
- `prompt-used.txt`
- `pipeline-meta.json`
- 可选 `qc-report.html`

### `$generate2dmap`

用于地图、场景和关卡资产。

常见输出：

- `base.png`
- `dressed-reference.png`
- `prop-pack.png`
- `props/`
- `placements.json`
- `collision.json`
- `zones.json`
- `layered-preview.png`
- Godot / Tiled / LDtk / Unity 等目标格式的 metadata 或场景草案

### `$generate2daudio`

用于生成和处理 2D 游戏音频资产。

常见输出：

- 单个 WAV 音效
- 每个音效对应的 `.analysis.json`
- 音效包 `audio-pack.json`
- 目录汇总 `analysis.json`
- Godot 可直接导入的 `AudioStreamWAV` 源文件

当前本地合成适合短音效，例如 UI、拾取、跳跃、命中、法术施放、法术循环和 impact。BGM、人声和复杂环境音建议后续接入专门音频模型或人工素材，再用本 skill 做清理、分析和交付。

## 示例音频素材

以下素材由 `$generate2daudio` 生成，已放入仓库示例目录，可作为 Godot 导入测试素材。

### Retro UI Pack

目录：[examples/audio/retro-ui-pack](./examples/audio/retro-ui-pack)

- [click.wav](./examples/audio/retro-ui-pack/click.wav)
- [confirm.wav](./examples/audio/retro-ui-pack/confirm.wav)
- [cancel.wav](./examples/audio/retro-ui-pack/cancel.wav)
- [error.wav](./examples/audio/retro-ui-pack/error.wav)
- [audio-pack.json](./examples/audio/retro-ui-pack/audio-pack.json)
- [analysis.json](./examples/audio/retro-ui-pack/analysis.json)

质量检查：4 个 WAV 均为 `-1 dBFS` 左右峰值，`clipping_samples = 0`，没有近似静音问题。

### Fantasy Fireball Godot Pack

目录：[examples/audio/fantasy-fireball-godot](./examples/audio/fantasy-fireball-godot)

- [spell-cast.wav](./examples/audio/fantasy-fireball-godot/spell-cast.wav)
- [spell-loop.wav](./examples/audio/fantasy-fireball-godot/spell-loop.wav)
- [fireball-loop-godot.wav](./examples/audio/fantasy-fireball-godot/fireball-loop-godot.wav)
- [spell-hit.wav](./examples/audio/fantasy-fireball-godot/spell-hit.wav)
- [audio-pack.json](./examples/audio/fantasy-fireball-godot/audio-pack.json)
- [analysis.json](./examples/audio/fantasy-fireball-godot/analysis.json)

Godot 建议：`spell-cast.wav` 和 `spell-hit.wav` 作为一次性音效触发，`fireball-loop-godot.wav` 用于循环播放。

## 安装

### Windows PowerShell

```powershell
git clone https://github.com/is0BIG/Agent-2D-Assets.git
cd .\Agent-2D-Assets
python -m pip install -r .\requirements.txt
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force `
  ".\skills\*" `
  "$env:USERPROFILE\.codex\skills\"
```

### macOS / Linux

```bash
git clone https://github.com/is0BIG/Agent-2D-Assets.git
cd ./Agent-2D-Assets
python3 -m pip install -r ./requirements.txt
mkdir -p ~/.codex/skills
cp -R ./skills/* ~/.codex/skills/
```

安装后请开启新的 Codex 会话，让 skills 重新加载。

## 示例提示词

### Sprite

```text
Use $generate2dsprite to create a 2x2 idle animation for a cute blue slime, top-down RPG style, transparent output and GIF preview.
```

```text
Use $generate2dsprite to create a side-view fire mage spell bundle with cast animation, projectile, and impact FX, pixel-inspired style, transparent PNG and GIF exports.
```

```text
Use $generate2dsprite to create a 4-direction top-down walk sheet for a tiny armored knight, 4x4 grid, consistent scale, transparent output.
```

### Map

```text
Use $generate2dmap to create a Godot-editable RPG map with TileMapLayer, separated props, encounter grass Area2D zones, collision StaticBody2D blockers, exit zones, and a debug player scene.
```

```text
Use $generate2dmap to create a playable side_scroll_mode platformer stage with parallax layers, stage-reference, separate platform_objects, collision metadata, camera bounds, and a stage-preview.
```

### Audio

```text
Use $generate2daudio to create a retro UI sound pack with click, confirm, cancel, and error WAV files plus engine-ready metadata.
```

```text
Use $generate2daudio to create a fantasy fireball audio bundle with cast, loop, and impact sounds for Godot.
```

## 本地脚本

### 处理 sprite sheet

```powershell
python .\skills\generate2dsprite\scripts\generate2dsprite.py process `
  --input .\raw-sheet.png `
  --target creature `
  --mode idle `
  --output-dir .\out\slime-idle `
  --rows 2 `
  --cols 2 `
  --shared-scale `
  --align bottom `
  --edge-feather 80 `
  --despill `
  --reject-edge-touch
```

### 切分 prop pack

```powershell
python .\skills\generate2dmap\scripts\extract_prop_pack.py `
  --input .\prop-pack.png `
  --rows 3 `
  --cols 3 `
  --output-dir .\out\props `
  --edge-feather 80 `
  --despill `
  --reject-edge-touch
```

### 生成音效包

```powershell
python .\skills\generate2daudio\scripts\synthesize_sfx.py `
  --preset ui-pack `
  --style retro `
  --output-dir .\outputs\audio\retro-ui-pack
```

### 分析音频

```powershell
python .\skills\generate2daudio\scripts\analyze_audio.py `
  --input .\outputs\audio\retro-ui-pack `
  --output .\outputs\audio\retro-ui-pack\analysis.json
```

## 开发与验证

运行测试：

```powershell
python -m unittest discover -s tests
```

当前测试覆盖：

- sprite 去背、切帧、metadata、贴边检测
- prop pack 切分和尺寸校验
- audio WAV 生成、处理、分析和 manifest

## 后续建议

如果目标是做完整 Godot 游戏，下一步最值得新增的 skill 是：

- `$assemblegodot2d`：把 sprite、map、audio 组装成 Godot `.tscn`、节点树和可运行 demo。
- `$generate2dgameplay`：生成玩家移动、敌人 AI、攻击、拾取、血量、冷却和关卡触发脚本。
- `$generate2dui`：生成 HUD、菜单、按钮、血条、技能栏、背包、对话框等 Godot UI。

## License

MIT. See [LICENSE](./LICENSE).
