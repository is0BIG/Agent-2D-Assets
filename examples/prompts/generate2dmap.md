# `$generate2dmap` 示例提示词

## 1. Godot 可编辑森林神社 RPG 地图

用途：展示 TileMapLayer、分离 props、碰撞、出口和 debug player。

```text
Use $generate2dmap to create a Godot-editable top-down RPG forest shrine map with TileMapLayer, separated props, encounter grass Area2D zones, collision StaticBody2D blockers, exit zones, player spawn, camera bounds, a debug player scene, and a layered preview.
```

推荐交付：

- `base.png`
- `props/`
- `placements.json`
- `collision.json`
- `zones.json`
- Godot scene 草案

## 2. 横版赛博运河关卡

用途：横版动作游戏、平台碰撞、视差背景。

```text
Use $generate2dmap to create a playable side_scroll_mode cyberpunk canal stage with parallax layers, shared stage_canvas, stage-reference, separate platform_objects, hazards, pickups, doors, camera bounds, collision metadata, and a stage-preview.
```

推荐交付：

- `sky.png`
- `far-bg.png`
- `mid-bg.png`
- `near-bg.png`
- `objects.json`
- `collision.json`
- `stage-preview.png`

## 3. 塔防森林通道

用途：Kingdom Rush-like 路线、防御塔槽位和波次入口。

```text
Use $generate2dmap to create a tower-defense forest pass map with a winding enemy route, build slots, separated props, blockers, spawn hook, exit hook, route metadata, tower-slot metadata, collision blockers, and a flattened preview for Godot.
```

推荐交付：

- route metadata
- tower slot metadata
- spawn / exit hooks
- blockers
- preview

## 4. 战术 RPG 小型战斗棋盘

用途：格子移动、地形消耗、战术战斗。

```text
Use $generate2dmap to create a compact tactical RPG battle grid, 10x8 cells, top-down fantasy ruins style, terrain types for normal ground, water, high ground, blocked rubble, and cover objects, with grid metadata, movement costs, collision, and a clean preview.
```

推荐交付：

- `grid.json`
- `terrain-costs.json`
- `collision.json`
- preview with optional debug overlay

## 5. Roguelike 房间块

用途：程序化拼接房间、出口 socket、碰撞边界。

```text
Use $generate2dmap to create a reusable roguelike dungeon room chunk, 16x12 tile layout, four possible exits, connection sockets, walkable floor, wall blockers, two prop variants, spawn markers as metadata only, collision metadata, and a QA preview.
```

推荐交付：

- `room-chunk.png`
- `chunk-metadata.json`
- exits / sockets
- blockers
- spawn markers as metadata
