# 示例产物总览

这里存放 15 条示例提示词对应的真实产出结果。`sprite/` 和 `map/` 的图片由内置图像生成得到原图后，再用本地脚本完成去背、切帧、GIF、prop 提取和 JSON 元数据；`audio/` 示例位于上一级 `examples/audio/`。

## Sprite 示例产物

| 示例 | 目录 | 主要产物 |
| --- | --- | --- |
| 蓝色史莱姆 2x2 idle | [sprite/slime-idle](./sprite/slime-idle) | `sheet-transparent.png`、4 张 frame PNG、`animation.gif`、`pipeline-meta.json` |
| 四方向骑士行走表 | [sprite/knight-walk](./sprite/knight-walk) | 4x4 透明 sheet、16 张 frame PNG、四方向 GIF、direction strips、metadata |
| 火法师法术包 | [sprite/fire-mage-spell-bundle](./sprite/fire-mage-spell-bundle) | `cast/`、`projectile/`、`impact/` 三个独立子包和 `bundle.json` |
| 冰爆 impact 2x2 | [sprite/ice-burst-impact](./sprite/ice-burst-impact) | 透明 sheet、4 张 frame PNG、`animation.gif`、metadata |
| 森林道具 3x3 prop pack | [sprite/forest-prop-pack](./sprite/forest-prop-pack) | 原始 prop pack、9 个透明 prop、`prop-pack.json` |

## Map 示例产物

| 示例 | 目录 | 主要产物 |
| --- | --- | --- |
| Godot 可编辑森林神社 RPG 地图 | [map/forest-shrine-godot](./map/forest-shrine-godot) | `base.png`、`layered-preview.png`、`placements.json`、`collision.json`、`zones.json` |
| 横版赛博运河关卡 | [map/cyber-canal-side-scroll](./map/cyber-canal-side-scroll) | parallax layer PNG、`stage-reference.png`、`stage-preview.png`、`objects.json`、`collision.json` |
| 塔防森林通道 | [map/tower-defense-forest-pass](./map/tower-defense-forest-pass) | `preview.png`、`route.json`、`tower-slots.json`、`collision.json` |
| 战术 RPG 小型战斗棋盘 | [map/tactical-ruins-grid](./map/tactical-ruins-grid) | `preview.png`、`grid.json`、`terrain-costs.json`、`collision.json` |
| Roguelike 房间块 | [map/roguelike-room-chunk](./map/roguelike-room-chunk) | `room-chunk.png`、`chunk-metadata.json`、`collision.json` |

## Audio 示例产物

| 示例 | 目录 |
| --- | --- |
| Retro UI Pack | [../audio/retro-ui-pack](../audio/retro-ui-pack) |
| Fantasy Fireball Godot Pack | [../audio/fantasy-fireball-godot](../audio/fantasy-fireball-godot) |
| Arcade Platformer Pack | [../audio/arcade-platformer-pack](../audio/arcade-platformer-pack) |
| Sci-Fi Combat Pack | [../audio/sci-fi-combat-pack](../audio/sci-fi-combat-pack) |
| Cozy Pickup Pack | [../audio/cozy-pickup-pack](../audio/cozy-pickup-pack) |

## 复现

`_raw/` 保存了本次示例使用的固定原图。要重新生成 sprite/map 的透明图、GIF 和 JSON：

```powershell
python .\examples\generated\build_example_outputs.py
```

脚本只做确定性后处理，不重新调用图像生成。
