# Agent-2D-Assets

言語：[English](./README.en.md) | [繁體中文](./README.zh-TW.md) | [简体中文](./README.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md)

<p align="center">
  <img src="./src/banner.png" alt="Agent-2D-Assets banner" width="900" />
</p>

<p align="center">
  <strong>Codex 向けの 2D ゲームアセット制作ワークフロー。Godot、Unity、または通常の 2D ゲームで使えるスプライト、マップ、オーディオ素材を生成します。</strong>
</p>

<p align="center">
  自然言語で依頼すると、Codex がアセット計画を立て、ローカルスクリプトが背景除去、フレーム分割、整列、品質チェック、音声処理、エクスポートを担当します。
</p>

## 謝辞

Agent-2D-Assets は、元の [0x0funky/agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) プロジェクトに敬意を表します。本プロジェクトの Codex 向け 2D sprite / map ワークフローの出発点は、そのリポジトリから着想を得ています。その方向性を引き継ぎつつ、ローカル処理スクリプト、Godot / Unity 連携ドキュメント、`generate2daudio` スキル、多言語ドキュメント、サンプル素材を拡張しています。元プロジェクトの著作権表示は [LICENSE](./LICENSE) に残しています。

## 特長

Agent-2D-Assets は単なるプロンプト集ではありません。Codex-first の 2D ゲームアセット制作パイプラインです。

| 種類 | Skill | 用途 |
| --- | --- | --- |
| スプライト / FX | [`generate2dsprite`](./skills/generate2dsprite) | キャラクター、モンスター、NPC、アイテム、魔法、投射物、ヒット FX、アニメーション |
| マップ / シーン | [`generate2dmap`](./skills/generate2dmap) | RPG マップ、レイヤー構成、TileMap、衝突判定、ゾーン、出口、Godot シーン案 |
| オーディオ / SFX | [`generate2daudio`](./skills/generate2daudio) | UI 音、戦闘 SFX、魔法バンドル、ループ音、WAV 分析、manifest |

## Version Roadmap

- `1.0`: 既存の 3 スキル構成を維持します。sprite sheet の背景除去と分割、map のレイヤー出力、audio WAV の生成と分析、Godot / Unity サンプルが含まれます。
- `1.1`: video-motion ワークフローを追加しました。walk、run、attack、cast、jump、hurt、death などの身体動作は、固定カメラの動画または PNG フレームから contact sheet でキーフレームを選び、透明フレーム、strip、sheet、GIF、Godot metadata として出力できます。

## Godot での利用

| Skill | Godot での使い方 | 出力 |
| --- | --- | --- |
| `$generate2dsprite` | `Sprite2D`、`AnimatedSprite2D`、`SpriteFrames`、`AnimationPlayer` にインポート | 透明 PNG、sprite sheet、frame PNG、GIF、`pipeline-meta.json` |
| `$generate2dmap` | `TileMapLayer`、`Sprite2D` props、`Area2D`、`StaticBody2D` の材料として使用 | base map、prop pack、placements、collision、zones、preview |
| `$generate2daudio` | WAV を `AudioStreamWAV` として直接インポート | WAV、`.analysis.json`、`audio-pack.json`、`analysis.json` |

推奨フロー：

```text
$generate2dsprite -> characters / enemies / FX
$generate2dmap    -> maps / collisions / spawn points / exits
$generate2daudio  -> UI / combat / magic / ambience
Godot             -> scenes / nodes / scripts / playable demo
```

## Showcase

### Godot Editable Map

<p align="center">
  <img src="./src/godot-editor.png" alt="Generate2DMap Godot editor scene" width="860" />
  <br />
  <strong>Godot editor scene：TileMapLayer、separated props、zones、collision、exits、debug player</strong>
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

### Layered Map Pipeline

<p align="center">
  <img src="./src/cyber-canal-layered-preview.png" alt="Layered cyberpunk canal RPG map preview" width="760" />
  <br />
  <strong>Flattened layered RPG map preview</strong>
</p>

## Audio Examples

これらは `$generate2daudio` で生成した Godot インポート用のサンプル素材です。

### Retro UI Pack

Directory: [examples/audio/retro-ui-pack](./examples/audio/retro-ui-pack)

- [click.wav](./examples/audio/retro-ui-pack/click.wav)
- [confirm.wav](./examples/audio/retro-ui-pack/confirm.wav)
- [cancel.wav](./examples/audio/retro-ui-pack/cancel.wav)
- [error.wav](./examples/audio/retro-ui-pack/error.wav)
- [audio-pack.json](./examples/audio/retro-ui-pack/audio-pack.json)
- [analysis.json](./examples/audio/retro-ui-pack/analysis.json)

### Fantasy Fireball Godot Pack

Directory: [examples/audio/fantasy-fireball-godot](./examples/audio/fantasy-fireball-godot)

- [spell-cast.wav](./examples/audio/fantasy-fireball-godot/spell-cast.wav)
- [spell-loop.wav](./examples/audio/fantasy-fireball-godot/spell-loop.wav)
- [fireball-loop-godot.wav](./examples/audio/fantasy-fireball-godot/fireball-loop-godot.wav)
- [spell-hit.wav](./examples/audio/fantasy-fireball-godot/spell-hit.wav)
- [audio-pack.json](./examples/audio/fantasy-fireball-godot/audio-pack.json)
- [analysis.json](./examples/audio/fantasy-fireball-godot/analysis.json)

Godot では `spell-cast.wav` と `spell-hit.wav` をワンショット音、`fireball-loop-godot.wav` をループ音として使うのがおすすめです。

## More Examples

Each skill has 5 copy-ready examples with purpose, prompt, expected outputs, and reproducible commands:

- [5 `$generate2dsprite` examples](./examples/prompts/generate2dsprite.md)
- [5 `$generate2dmap` examples](./examples/prompts/generate2dmap.md)
- [5 `$generate2daudio` examples](./examples/prompts/generate2daudio.md)
- [Example overview](./examples/prompts/README.md)
- [Generated output overview: PNG / GIF / WAV / JSON](./examples/generated/README.md)

実際のサンプル出力は [examples/generated](./examples/generated) に、WAV パックは [examples/audio](./examples/audio) にあります。

## Install

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

## Suggested Prompts

```text
Use $generate2dsprite to create a 2x2 idle animation for a cute blue slime, top-down RPG style, transparent output and GIF preview.
```

```text
Use $generate2dsprite with the 1.1 video_motion workflow to convert a fixed-camera green-screen sword slash video into transparent frames, a sprite strip, a sprite sheet, GIF preview, and Godot metadata.
```

```text
Use $generate2dmap to create a Godot-editable RPG map with TileMapLayer, separated props, encounter grass Area2D zones, collision StaticBody2D blockers, exit zones, and a debug player scene.
```

```text
Use $generate2daudio to create a fantasy fireball audio bundle with cast, loop, and impact sounds for Godot.
```

## Development

```powershell
python -m unittest discover -s tests
```

## Next Skills

- `$assemblegodot2d`: assemble sprites, maps, and audio into Godot `.tscn` scenes.
- `$generate2dgameplay`: generate movement, combat, pickups, HP, enemy AI, and level triggers.
- `$generate2dui`: generate HUD, menus, health bars, skill slots, inventory, and dialog UI.

## License

MIT. See [LICENSE](./LICENSE).
