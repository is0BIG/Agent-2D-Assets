# `$generate2dsprite` 示例提示词

## 1. 蓝色史莱姆 2x2 idle

用途：RPG 初级怪物、演示透明 PNG 和 GIF 导出。

示例产物：[../generated/sprite/slime-idle](../generated/sprite/slime-idle)

```text
Use $generate2dsprite to create a 2x2 idle animation for a cute blue slime, top-down RPG style, consistent scale, centered body, transparent output, frame PNGs, and GIF preview.
```

推荐输出：

- `sheet-transparent.png`
- `frame-1.png` 到 `frame-4.png`
- `animation.gif`
- `pipeline-meta.json`

## 2. 四方向骑士行走表

用途：Godot `AnimatedSprite2D` 或 `AnimationPlayer` 的玩家角色基础素材。

示例产物：[../generated/sprite/knight-walk](../generated/sprite/knight-walk)

```text
Use $generate2dsprite to create a 4-direction top-down walk sheet for a tiny armored knight, 4x4 grid, directions down/left/right/up, consistent scale, feet aligned, transparent PNG output, per-direction strips, per-direction GIF previews, and metadata for Godot.
```

推荐输出：

- 4x4 transparent sheet
- `down.gif` / `left.gif` / `right.gif` / `up.gif`
- per-direction frame folders
- `pipeline-meta.json`

## 3. 火法师法术包

用途：把角色施法、投射物和命中特效拆成可复用素材。

示例产物：[../generated/sprite/fire-mage-spell-bundle](../generated/sprite/fire-mage-spell-bundle)

```text
Use $generate2dsprite to create a side-view fire mage spell bundle with body-only cast animation, separate fire projectile, separate impact burst, pixel-inspired fantasy style, transparent PNG exports, GIF previews, and prompt-used metadata.
```

推荐拆分：

- `cast/`
- `projectile/`
- `impact/`
- 每个子目录独立处理和质检

## 4. 冰爆 impact 2x2

用途：技能命中、陷阱触发、宝箱开启等短 FX。

示例产物：[../generated/sprite/ice-burst-impact](../generated/sprite/ice-burst-impact)

```text
Use $generate2dsprite to create a 2x2 impact animation for a blue ice burst, top-down RPG combat style, no character body, strong readable silhouette, transparent output, centered frames, and GIF preview.
```

推荐输出：

- `sheet-transparent.png`
- 4 个 frame PNG
- `animation.gif`

## 5. 森林道具 3x3 prop pack

用途：给 `$generate2dmap` 的分层地图提供可复用透明 props。

示例产物：[../generated/sprite/forest-prop-pack](../generated/sprite/forest-prop-pack)

```text
Use $generate2dsprite to create a 3x3 transparent forest prop pack for a clean HD top-down RPG map: small rock, stump, bush, mushroom cluster, signpost, crate, flower patch, lantern, and broken pot. Keep each prop centered in its cell with safe padding and a solid magenta background for local extraction.
```

推荐后处理：

```powershell
python .\skills\generate2dmap\scripts\extract_prop_pack.py `
  --input .\prop-pack.png `
  --rows 3 `
  --cols 3 `
  --output-dir .\out\forest-props `
  --edge-feather 80 `
  --despill `
  --reject-edge-touch
```
