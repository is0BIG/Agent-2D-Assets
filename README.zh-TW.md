# Agent-2D-Assets

語言：[English](./README.en.md) | [繁體中文](./README.zh-TW.md) | [简体中文](./README.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md)

<p align="center">
  <img src="./src/banner.png" alt="Agent-2D-Assets banner" width="900" />
</p>

<p align="center">
  <strong>面向 Codex 的 2D 遊戲資產工作流：產出可用於 Godot、Unity 或原生 2D 專案的角色、地圖與音訊素材。</strong>
</p>

<p align="center">
  用自然語言描述需求。Codex 負責資產規劃與生成，本地腳本負責去背、切幀、對齊、品質檢查、音訊處理與匯出。
</p>

## 專案特點

Agent-2D-Assets 不是單純的提示詞集合，而是一套 Codex-first 的 2D 遊戲資產流水線。

| 類型 | Skill | 適合生成 |
| --- | --- | --- |
| 角色與特效 | [`generate2dsprite`](./skills/generate2dsprite) | 角色、怪物、NPC、道具、法術、投射物、命中特效、動畫幀 |
| 地圖與場景 | [`generate2dmap`](./skills/generate2dmap) | RPG 地圖、分層場景、TileMap、碰撞、區域、出口、Godot 場景草案 |
| 音訊與音效 | [`generate2daudio`](./skills/generate2daudio) | UI 音效、戰鬥音效、法術音效包、循環音、WAV 分析與 manifest |

## Godot 可用性

| Skill | Godot 用法 | 典型輸出 |
| --- | --- | --- |
| `$generate2dsprite` | 匯入 `Sprite2D`、`AnimatedSprite2D`、`SpriteFrames` 或 `AnimationPlayer` | 透明 PNG、sprite sheet、frame PNG、GIF、`pipeline-meta.json` |
| `$generate2dmap` | 組成 `TileMapLayer`、`Sprite2D` props、`Area2D` 區域與 `StaticBody2D` 碰撞 | base map、prop pack、placements、collision、zones、preview |
| `$generate2daudio` | WAV 可直接作為 `AudioStreamWAV`，用於 `AudioStreamPlayer` 或 `AudioStreamPlayer2D` | WAV、`.analysis.json`、`audio-pack.json`、`analysis.json` |

建議工作流：

```text
$generate2dsprite -> 角色 / 敵人 / FX
$generate2dmap    -> 地圖 / 碰撞 / 出生點 / 出口
$generate2daudio  -> UI / 戰鬥 / 法術 / 環境音
Godot             -> 組裝節點、場景、腳本與可執行 demo
```

## Showcase

### Godot 可編輯地圖

<p align="center">
  <img src="./src/godot-editor.png" alt="Generate2DMap Godot editor scene" width="860" />
  <br />
  <strong>Godot editor scene：TileMapLayer、獨立 props、區域、碰撞、出口與 debug player</strong>
</p>

### Sprite Sheets And FX

<table>
  <tr>
    <td align="center" width="25%"><img src="./src/goku-kame.gif" alt="Goku Kamehameha sprite animation" width="170" /><br /><strong>Attack animation</strong></td>
    <td align="center" width="25%"><img src="./src/naruto-rasengan.gif" alt="Naruto Rasengan sprite animation" width="170" /><br /><strong>Character action</strong></td>
    <td align="center" width="25%"><img src="./src/cast.gif" alt="Fire mage cast animation" width="150" /><br /><strong>Spell cast</strong></td>
    <td align="center" width="25%"><img src="./src/projectile.gif" alt="Fire mage projectile animation" width="150" /><br /><strong>Projectile</strong></td>
  </tr>
</table>

### 分層地圖流程

<p align="center">
  <img src="./src/cyber-canal-layered-preview.png" alt="Layered cyberpunk canal RPG map preview" width="760" />
  <br />
  <strong>Flattened layered RPG map preview</strong>
</p>

## 音訊示例素材

以下素材由 `$generate2daudio` 產生，可直接作為 Godot 匯入測試素材。

### Retro UI Pack

目錄：[examples/audio/retro-ui-pack](./examples/audio/retro-ui-pack)

- [click.wav](./examples/audio/retro-ui-pack/click.wav)
- [confirm.wav](./examples/audio/retro-ui-pack/confirm.wav)
- [cancel.wav](./examples/audio/retro-ui-pack/cancel.wav)
- [error.wav](./examples/audio/retro-ui-pack/error.wav)
- [audio-pack.json](./examples/audio/retro-ui-pack/audio-pack.json)
- [analysis.json](./examples/audio/retro-ui-pack/analysis.json)

### Fantasy Fireball Godot Pack

目錄：[examples/audio/fantasy-fireball-godot](./examples/audio/fantasy-fireball-godot)

- [spell-cast.wav](./examples/audio/fantasy-fireball-godot/spell-cast.wav)
- [spell-loop.wav](./examples/audio/fantasy-fireball-godot/spell-loop.wav)
- [fireball-loop-godot.wav](./examples/audio/fantasy-fireball-godot/fireball-loop-godot.wav)
- [spell-hit.wav](./examples/audio/fantasy-fireball-godot/spell-hit.wav)
- [audio-pack.json](./examples/audio/fantasy-fireball-godot/audio-pack.json)
- [analysis.json](./examples/audio/fantasy-fireball-godot/analysis.json)

Godot 建議：`spell-cast.wav` 與 `spell-hit.wav` 作為一次性音效，`fireball-loop-godot.wav` 用於循環播放。

## 安裝

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

## 示例提示詞

```text
Use $generate2dsprite to create a 2x2 idle animation for a cute blue slime, top-down RPG style, transparent output and GIF preview.
```

```text
Use $generate2dmap to create a Godot-editable RPG map with TileMapLayer, separated props, encounter grass Area2D zones, collision StaticBody2D blockers, exit zones, and a debug player scene.
```

```text
Use $generate2daudio to create a fantasy fireball audio bundle with cast, loop, and impact sounds for Godot.
```

## 開發與驗證

```powershell
python -m unittest discover -s tests
```

## 後續建議

- `$assemblegodot2d`：把 sprite、map、audio 組裝成 Godot `.tscn`、節點樹與可執行 demo。
- `$generate2dgameplay`：生成玩家移動、敵人 AI、攻擊、拾取、血量與關卡觸發腳本。
- `$generate2dui`：生成 HUD、選單、血條、技能欄、背包與對話框。

## License

MIT. See [LICENSE](./LICENSE).
