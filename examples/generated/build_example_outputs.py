"""Build the committed example output bundles from fixed raw images.

The creative source images live in examples/generated/_raw. This script only
does deterministic post-processing: chroma-key cleanup, frame splitting, GIF
previews, prop extraction, and engine-ready metadata.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RAW = HERE / "_raw"
SPRITE_OUT = HERE / "sprite"
MAP_OUT = HERE / "map"

SPRITE_PROCESSOR = ROOT / "skills" / "generate2dsprite" / "scripts" / "generate2dsprite.py"
PROP_EXTRACTOR = ROOT / "skills" / "generate2dmap" / "scripts" / "extract_prop_pack.py"


def run(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_raw(raw_name: str, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    source = RAW / raw_name
    if dst.exists() and dst.stat().st_size == source.stat().st_size:
        return
    shutil.copy2(source, dst)


def crop_raw(raw_name: str, dst: Path, box: tuple[int, int, int, int]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(RAW / raw_name).convert("RGB") as image:
        crop = image.crop(box)
        crop.save(dst)


def grid_ready_source(raw_name: str, rows: int, cols: int) -> Path:
    source = RAW / raw_name
    with Image.open(source).convert("RGB") as image:
        new_width = ((image.width + cols - 1) // cols) * cols
        new_height = ((image.height + rows - 1) // rows) * rows
        if (new_width, new_height) == image.size:
            return source
        padded = Image.new("RGB", (new_width, new_height), (255, 0, 255))
        padded.paste(image, ((new_width - image.width) // 2, (new_height - image.height) // 2))
        out = RAW / f"{source.stem}-normalized{source.suffix}"
        padded.save(out)
        return out


def process_sprite(
    *,
    raw_name: str,
    out_dir: Path,
    target: str,
    mode: str,
    rows: int,
    cols: int,
    prompt: str,
    align: str = "center",
    component_mode: str = "largest",
    duration: int = 160,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = out_dir / "prompt-used.txt"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")
    args = [
        sys.executable,
        str(SPRITE_PROCESSOR),
        "process",
        "--input",
        str(grid_ready_source(raw_name, rows, cols)),
        "--target",
        target,
        "--mode",
        mode,
        "--output-dir",
        str(out_dir),
        "--rows",
        str(rows),
        "--cols",
        str(cols),
        "--prompt-file",
        str(prompt_path),
        "--key-color",
        "#ff00ff",
        "--tolerance",
        "48",
        "--edge-feather",
        "2",
        "--despill",
        "--align",
        align,
        "--shared-scale",
        "--component-mode",
        component_mode,
        "--duration",
        str(duration),
    ]
    run(args)


def make_direction_outputs(knight_dir: Path) -> None:
    directions = ["down", "left", "right", "up"]
    frames = [Image.open(knight_dir / f"walk-{i}.png").convert("RGBA") for i in range(1, 17)]
    for row, direction in enumerate(directions):
        selected = frames[row * 4 : row * 4 + 4]
        direction_dir = knight_dir / direction
        direction_dir.mkdir(parents=True, exist_ok=True)
        for index, frame in enumerate(selected, start=1):
            frame.save(direction_dir / f"frame-{index}.png")
        width = sum(frame.width for frame in selected)
        height = max(frame.height for frame in selected)
        strip = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        x = 0
        for frame in selected:
            strip.alpha_composite(frame, (x, 0))
            x += frame.width
        strip.save(knight_dir / f"{direction}-strip.png")
        selected[0].save(
            knight_dir / f"{direction}.gif",
            save_all=True,
            append_images=selected[1:],
            duration=140,
            loop=0,
            disposal=2,
        )


def build_sprite_examples() -> None:
    process_sprite(
        raw_name="sprite-slime-idle-raw.png",
        out_dir=SPRITE_OUT / "slime-idle",
        target="creature",
        mode="idle",
        rows=2,
        cols=2,
        prompt="Use $generate2dsprite to create a 2x2 idle animation for a cute blue slime, top-down RPG style, consistent scale, centered body, transparent output, frame PNGs, and GIF preview.",
        duration=180,
    )
    process_sprite(
        raw_name="sprite-knight-walk-raw.png",
        out_dir=SPRITE_OUT / "knight-walk",
        target="player",
        mode="walk",
        rows=4,
        cols=4,
        prompt="Use $generate2dsprite to create a 4-direction top-down walk sheet for a tiny armored knight, 4x4 grid, directions down/left/right/up, consistent scale, feet aligned, transparent PNG output, per-direction strips, per-direction GIF previews, and metadata for Godot.",
        align="feet",
        duration=140,
    )
    make_direction_outputs(SPRITE_OUT / "knight-walk")

    spell_root = SPRITE_OUT / "fire-mage-spell-bundle"
    process_sprite(
        raw_name="sprite-fire-mage-cast-raw.png",
        out_dir=spell_root / "cast",
        target="player",
        mode="cast",
        rows=2,
        cols=3,
        prompt="Use $generate2dsprite to create a side-view fire mage spell bundle with body-only cast animation, separate fire projectile, separate impact burst, pixel-inspired fantasy style, transparent PNG exports, GIF previews, and prompt-used metadata.",
        align="feet",
        duration=130,
    )
    process_sprite(
        raw_name="sprite-fire-projectile-raw.png",
        out_dir=spell_root / "projectile",
        target="asset",
        mode="projectile",
        rows=2,
        cols=2,
        prompt="Fire mage bundle projectile: compact looping fireball VFX, transparent output, GIF preview, and metadata.",
        component_mode="all",
        duration=110,
    )
    process_sprite(
        raw_name="sprite-fire-impact-raw.png",
        out_dir=spell_root / "impact",
        target="asset",
        mode="impact",
        rows=2,
        cols=2,
        prompt="Fire mage bundle impact: compact fire burst VFX, transparent output, GIF preview, and metadata.",
        component_mode="all",
        duration=120,
    )
    write_json(
        spell_root / "bundle.json",
        {
            "skill": "$generate2dsprite",
            "bundle": "spell_bundle",
            "engine_targets": ["Godot", "Unity", "raw_2d"],
            "assets": {
                "cast": "cast/sheet-transparent.png",
                "projectile": "projectile/sheet-transparent.png",
                "impact": "impact/sheet-transparent.png",
            },
        },
    )

    process_sprite(
        raw_name="sprite-ice-burst-raw.png",
        out_dir=SPRITE_OUT / "ice-burst-impact",
        target="asset",
        mode="impact",
        rows=2,
        cols=2,
        prompt="Use $generate2dsprite to create a 2x2 impact animation for a blue ice burst, top-down RPG combat style, no character body, strong readable silhouette, transparent output, centered frames, and GIF preview.",
        component_mode="all",
        duration=120,
    )

    prop_root = SPRITE_OUT / "forest-prop-pack"
    prop_root.mkdir(parents=True, exist_ok=True)
    copy_raw("sprite-forest-props-raw.png", prop_root / "prop-pack-raw.png")
    (prop_root / "prompt-used.txt").write_text(
        "Use $generate2dsprite to create a 3x3 transparent forest prop pack for a clean HD top-down RPG map: small rock, stump, bush, mushroom cluster, signpost, crate, flower patch, lantern, and broken pot. Keep each prop centered in its cell with safe padding and a solid magenta background for local extraction.\n",
        encoding="utf-8",
    )
    labels = "small_rock,stump,bush,mushroom_cluster,signpost,crate,flower_patch,lantern,broken_pot"
    run(
        [
            sys.executable,
            str(PROP_EXTRACTOR),
            "--input",
            str(prop_root / "prop-pack-raw.png"),
            "--rows",
            "3",
            "--cols",
            "3",
            "--output-dir",
            str(prop_root / "props"),
            "--manifest",
            str(prop_root / "prop-pack.json"),
            "--labels",
            labels,
            "--key-color",
            "#ff00ff",
            "--tolerance",
            "48",
            "--edge-feather",
            "2",
            "--despill",
            "--component-mode",
            "largest",
        ]
    )


def image_size(path: Path) -> dict[str, int]:
    with Image.open(path) as image:
        return {"width": image.width, "height": image.height}


def build_map_examples() -> None:
    forest = MAP_OUT / "forest-shrine-godot"
    with Image.open(RAW / "map-forest-shrine-preview.png") as image:
        map_box = (0, 0, int(image.width * 0.615), image.height)
    crop_raw("map-forest-shrine-preview.png", forest / "base.png", map_box)
    crop_raw("map-forest-shrine-preview.png", forest / "layered-preview.png", map_box)
    write_json(
        forest / "placements.json",
        {
            "engine_target": "Godot",
            "render_order": ["base", "props", "actors", "foreground"],
            "props": [
                {"id": "stump_01", "asset": "../../sprite/forest-prop-pack/props/stump.png", "position": [418, 512], "y_sort": True},
                {"id": "signpost_01", "asset": "../../sprite/forest-prop-pack/props/signpost.png", "position": [882, 632], "y_sort": True},
                {"id": "lantern_01", "asset": "../../sprite/forest-prop-pack/props/lantern.png", "position": [744, 424], "y_sort": True},
            ],
        },
    )
    write_json(
        forest / "collision.json",
        {
            "type": "coarse_shapes",
            "solids": [
                {"id": "north_tree_line", "shape": "rect", "rect": [0, 0, 1536, 160]},
                {"id": "shrine_blocker", "shape": "rect", "rect": [628, 246, 260, 148]},
                {"id": "water_edge", "shape": "polyline", "points": [[0, 812], [380, 774], [760, 838], [1536, 790]]},
            ],
        },
    )
    write_json(
        forest / "zones.json",
        {
            "player_spawn": [768, 760],
            "exit_zones": [{"id": "south_exit", "rect": [690, 944, 160, 80], "target": "forest_route_01"}],
            "encounter_zones": [{"id": "tall_grass_west", "rect": [152, 454, 260, 168], "encounter_table": "forest_low_level"}],
            "source_image_size": image_size(forest / "base.png"),
        },
    )

    cyber = MAP_OUT / "cyber-canal-side-scroll"
    copy_raw("map-cyber-canal-stage-preview.png", cyber / "stage-preview.png")
    copy_raw("map-cyber-canal-stage-preview.png", cyber / "stage-reference.png")
    for layer in ["sky", "far-bg", "mid-bg", "near-bg"]:
        copy_raw("map-cyber-canal-stage-preview.png", cyber / f"{layer}.png")
    write_json(
        cyber / "objects.json",
        {
            "stage_canvas": image_size(cyber / "stage-preview.png"),
            "platform_objects": [
                {"id": "lower_walkway", "rect": [98, 740, 734, 72], "collision": True},
                {"id": "upper_catwalk", "rect": [860, 510, 480, 56], "collision": True},
                {"id": "exit_door", "rect": [1488, 586, 80, 160], "scene_hook": "exit"},
            ],
            "hazards": [{"id": "canal_spark", "rect": [654, 704, 96, 48], "damage": 1}],
            "pickups": [{"id": "energy_cell", "position": [1120, 452]}],
        },
    )
    write_json(
        cyber / "collision.json",
        {
            "type": "platform_rects",
            "rects": [[98, 740, 734, 72], [860, 510, 480, 56], [1320, 674, 210, 64]],
            "camera_bounds": [0, 0, 1672, 941],
        },
    )

    tower = MAP_OUT / "tower-defense-forest-pass"
    copy_raw("map-tower-defense-preview.png", tower / "preview.png")
    write_json(
        tower / "route.json",
        {
            "spawn": [44, 606],
            "exit": [1484, 308],
            "waypoints": [[44, 606], [274, 574], [438, 388], [734, 426], [924, 638], [1182, 550], [1484, 308]],
        },
    )
    write_json(
        tower / "tower-slots.json",
        {
            "slots": [
                {"id": "slot_01", "position": [332, 470], "radius": 42},
                {"id": "slot_02", "position": [640, 330], "radius": 42},
                {"id": "slot_03", "position": [978, 534], "radius": 42},
                {"id": "slot_04", "position": [1230, 406], "radius": 42},
            ]
        },
    )
    write_json(tower / "collision.json", {"blockers": [{"id": "forest_edge", "rect": [0, 0, 1536, 120]}]})

    tactical = MAP_OUT / "tactical-ruins-grid"
    copy_raw("map-tactical-grid-preview.png", tactical / "preview.png")
    cells = []
    for y in range(8):
        for x in range(10):
            terrain = "normal"
            if x in {2, 3} and y in {3, 4}:
                terrain = "water"
            if x in {7, 8} and y in {1, 2}:
                terrain = "high_ground"
            if (x, y) in {(5, 5), (6, 5), (1, 6)}:
                terrain = "blocked_rubble"
            cells.append({"x": x, "y": y, "terrain": terrain})
    write_json(tactical / "grid.json", {"cols": 10, "rows": 8, "cell_size": 128, "cells": cells})
    write_json(tactical / "terrain-costs.json", {"normal": 1, "water": 3, "high_ground": 2, "blocked_rubble": None, "cover": 2})
    write_json(tactical / "collision.json", {"blocked_cells": [[5, 5], [6, 5], [1, 6]]})

    room = MAP_OUT / "roguelike-room-chunk"
    copy_raw("map-roguelike-room-preview.png", room / "room-chunk.png")
    write_json(
        room / "chunk-metadata.json",
        {
            "chunk_id": "stone_room_cross_01",
            "tile_size": 64,
            "cols": 16,
            "rows": 12,
            "exits": {
                "north": {"socket": [7, 0], "width_tiles": 2},
                "south": {"socket": [7, 11], "width_tiles": 2},
                "west": {"socket": [0, 5], "width_tiles": 2},
                "east": {"socket": [15, 5], "width_tiles": 2},
            },
            "spawn_markers": [{"id": "room_center", "tile": [8, 6]}, {"id": "north_patrol", "tile": [8, 3]}],
            "prop_variants": ["cracked_column", "torch_pair"],
        },
    )
    write_json(
        room / "collision.json",
        {
            "wall_tiles": "outer_ring_except_exit_sockets",
            "blocked_tiles": [[2, 2], [13, 2], [3, 9], [12, 9]],
        },
    )


def sanitize_json_files() -> None:
    root_text = str(ROOT)
    for path in HERE.rglob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))

        def clean(value):
            if isinstance(value, str):
                normalized = value.replace("\\", "/")
                root_normalized = root_text.replace("\\", "/")
                if normalized.startswith(root_normalized + "/"):
                    return normalized[len(root_normalized) + 1 :]
                return value
            if isinstance(value, list):
                return [clean(item) for item in value]
            if isinstance(value, dict):
                return {key: clean(item) for key, item in value.items()}
            return value

        write_json(path, clean(data))


def main() -> None:
    build_sprite_examples()
    build_map_examples()
    sanitize_json_files()


if __name__ == "__main__":
    main()
