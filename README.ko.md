# Agent-2D-Assets

언어: [English](./README.en.md) | [繁體中文](./README.zh-TW.md) | [简体中文](./README.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md)

<p align="center">
  <img src="./src/banner.png" alt="Agent-2D-Assets banner" width="900" />
</p>

<p align="center">
  <strong>Codex용 2D 게임 에셋 워크플로입니다. Godot, Unity, 일반 2D 게임 프로젝트에서 쓸 수 있는 스프라이트, 맵, 오디오 에셋을 생성합니다.</strong>
</p>

<p align="center">
  자연어로 요청하면 Codex가 에셋 계획을 세우고, 로컬 스크립트가 배경 제거, 프레임 분할, 정렬, 품질 검사, 오디오 처리, 내보내기를 담당합니다.
</p>

## 특징

Agent-2D-Assets는 단순한 프롬프트 모음이 아니라 Codex-first 2D 게임 에셋 제작 파이프라인입니다.

| 종류 | Skill | 용도 |
| --- | --- | --- |
| 스프라이트 / FX | [`generate2dsprite`](./skills/generate2dsprite) | 캐릭터, 몬스터, NPC, 아이템, 마법, 투사체, 히트 FX, 애니메이션 |
| 맵 / 씬 | [`generate2dmap`](./skills/generate2dmap) | RPG 맵, 레이어드 씬, TileMap, 충돌, 구역, 출구, Godot 씬 초안 |
| 오디오 / SFX | [`generate2daudio`](./skills/generate2daudio) | UI 사운드, 전투 SFX, 마법 사운드 번들, 루프 사운드, WAV 분석, manifest |

## Godot 사용성

| Skill | Godot에서의 사용 | 출력 |
| --- | --- | --- |
| `$generate2dsprite` | `Sprite2D`, `AnimatedSprite2D`, `SpriteFrames`, `AnimationPlayer`에 가져오기 | 투명 PNG, sprite sheet, frame PNG, GIF, `pipeline-meta.json` |
| `$generate2dmap` | `TileMapLayer`, `Sprite2D` props, `Area2D`, `StaticBody2D` 구성에 사용 | base map, prop pack, placements, collision, zones, preview |
| `$generate2daudio` | WAV를 `AudioStreamWAV`로 직접 가져오기 | WAV, `.analysis.json`, `audio-pack.json`, `analysis.json` |

추천 흐름:

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
  <strong>Godot editor scene: TileMapLayer, separated props, zones, collision, exits, debug player</strong>
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

다음 샘플은 `$generate2daudio`로 생성했으며 Godot 가져오기 테스트에 바로 사용할 수 있습니다.

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

Godot에서는 `spell-cast.wav`와 `spell-hit.wav`를 일회성 효과음으로, `fireball-loop-godot.wav`를 루프 사운드로 쓰는 것을 권장합니다.

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

- `$assemblegodot2d`: sprites, maps, audio를 Godot `.tscn` 씬으로 조립합니다.
- `$generate2dgameplay`: 이동, 전투, 픽업, HP, 적 AI, 레벨 트리거를 생성합니다.
- `$generate2dui`: HUD, 메뉴, 체력바, 스킬 슬롯, 인벤토리, 대화 UI를 생성합니다.

## License

MIT. See [LICENSE](./LICENSE).
