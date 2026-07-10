# `$generate2daudio` 示例提示词

## 1. Retro UI Pack

真实素材目录：[../audio/retro-ui-pack](../audio/retro-ui-pack)

```text
Use $generate2daudio to create a retro UI sound pack with click, confirm, cancel, and error WAV files plus engine-ready metadata.
```

推荐用途：

- 菜单选择
- 确认 / 取消
- 错误提示

## 2. Fantasy Fireball Godot Pack

真实素材目录：[../audio/fantasy-fireball-godot](../audio/fantasy-fireball-godot)

```text
Use $generate2daudio to create a fantasy fireball audio bundle with cast, loop, and impact sounds for Godot.
```

推荐用途：

- `spell-cast.wav`：施法瞬间
- `fireball-loop-godot.wav`：飞行循环音
- `spell-hit.wav`：命中爆发

## 3. Arcade Platformer Pack

真实素材目录：[../audio/arcade-platformer-pack](../audio/arcade-platformer-pack)

```text
Use $generate2daudio to create an arcade platformer sound pack with jump, land, pickup, hit, and powerup WAV files, short responsive timing, no clipping, and engine-ready metadata.
```

本地复现：

```powershell
python .\skills\generate2daudio\scripts\synthesize_sfx.py `
  --preset platformer-pack `
  --style arcade `
  --output-dir .\examples\audio\arcade-platformer-pack
```

## 4. Sci-Fi Combat Pack

真实素材目录：[../audio/sci-fi-combat-pack](../audio/sci-fi-combat-pack)

```text
Use $generate2daudio to create a sci-fi combat sound pack with laser shot, small explosion, and hit impact WAV files, punchy transient, normalized peaks, and analysis metadata for Godot.
```

推荐用途：

- 射击
- 爆炸
- 命中反馈

## 5. Cozy Pickup Pack

真实素材目录：[../audio/cozy-pickup-pack](../audio/cozy-pickup-pack)

```text
Use $generate2daudio to create a cozy pickup and reward sound pack with pickup, powerup, and confirm WAV files, soft tone, low harshness, short duration, and engine-ready analysis metadata.
```

推荐用途：

- 收集金币 / 果实
- 奖励弹窗
- 轻量确认音
