#!/usr/bin/env python3
"""Convert selected full-canvas animation frames into a game-ready sprite strip."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def parse_color(value: str) -> tuple[int, int, int]:
    text = value.strip()
    if text.startswith("#"):
        text = text[1:]
    if "," in text:
        parts = [int(part.strip()) for part in text.split(",")]
        if len(parts) == 3 and all(0 <= part <= 255 for part in parts):
            return parts[0], parts[1], parts[2]
    if len(text) == 6:
        return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)
    raise ValueError(f"Invalid color '{value}'. Use #RRGGBB or R,G,B.")


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def load_indices(path: Path | None) -> list[int] | None:
    if path is None:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("frames") or data.get("indices")
    if not isinstance(data, list):
        raise ValueError("Frame index file must be a list or an object with frames/indices.")
    indices = [int(value) for value in data]
    if any(index < 0 for index in indices):
        raise ValueError("Frame indices are zero-based and must not be negative.")
    return indices


def collect_frames(frames_dir: Path, pattern: str, indices: list[int] | None) -> list[Path]:
    files = sorted(frames_dir.glob(pattern), key=natural_key)
    if not files:
        raise FileNotFoundError(f"No frames matched {frames_dir / pattern}.")
    if indices is None:
        return files
    missing = [index for index in indices if index >= len(files)]
    if missing:
        raise IndexError(f"Frame index out of range: {missing}; available frame count is {len(files)}.")
    return [files[index] for index in indices]


def remove_key_color(
    image: Image.Image,
    *,
    key_color: tuple[int, int, int],
    tolerance: int,
    edge_feather: int,
    despill: bool,
) -> Image.Image:
    rgba = image.convert("RGBA")
    arr = np.array(rgba).astype(np.float32)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]
    key = np.array(key_color, dtype=np.float32)
    dist = np.linalg.norm(rgb - key, axis=2)

    hard = dist <= tolerance
    alpha[hard] = 0
    if edge_feather > 0:
        soft = (dist > tolerance) & (dist <= tolerance + edge_feather)
        factor = (dist[soft] - tolerance) / max(1, edge_feather)
        alpha[soft] = np.minimum(alpha[soft], factor * 255)

    if despill:
        near = dist <= tolerance + max(edge_feather, 1)
        strength = np.clip(1.0 - (dist / max(1, tolerance + edge_feather)), 0.0, 1.0)
        for channel in range(3):
            rgb[:, :, channel] = np.where(
                near,
                rgb[:, :, channel] - (key[channel] * strength * 0.35),
                rgb[:, :, channel],
            )

    arr[:, :, :3] = np.clip(rgb, 0, 255)
    arr[:, :, 3] = np.clip(alpha, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def fit_full_canvas(image: Image.Image, size: tuple[int, int]) -> tuple[Image.Image, float, tuple[int, int]]:
    target_w, target_h = size
    source_w, source_h = image.size
    scale = min(target_w / source_w, target_h / source_h)
    new_size = (max(1, round(source_w * scale)), max(1, round(source_h * scale)))
    resized = image.resize(new_size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    paste = ((target_w - new_size[0]) // 2, (target_h - new_size[1]) // 2)
    canvas.paste(resized, paste, resized)
    return canvas, scale, paste


def alpha_bbox(image: Image.Image) -> list[int] | None:
    bbox = image.getbbox()
    return list(bbox) if bbox else None


def bbox_touches_edge(bbox: list[int] | None, width: int, height: int, margin: int) -> bool:
    if bbox is None:
        return False
    left, top, right, bottom = bbox
    return left <= margin or top <= margin or right >= width - margin or bottom >= height - margin


def compose_sheet(frames: list[Image.Image], cols: int, cell_size: tuple[int, int]) -> Image.Image:
    if cols <= 0:
        raise ValueError("--sheet-cols must be positive.")
    rows = math.ceil(len(frames) / cols)
    cell_w, cell_h = cell_size
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        row, col = divmod(index, cols)
        sheet.paste(frame, (col * cell_w, row * cell_h), frame)
    return sheet


def make_checker_preview(frames: list[Image.Image], cols: int, cell_size: tuple[int, int]) -> Image.Image:
    transparent = compose_sheet(frames, cols, cell_size)
    checker = Image.new("RGBA", transparent.size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(checker)
    tile = 16
    for y in range(0, checker.height, tile):
        for x in range(0, checker.width, tile):
            shade = 220 if ((x // tile) + (y // tile)) % 2 else 245
            draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(shade, shade, shade, 255))
    checker.alpha_composite(transparent)
    return checker


def save_transparent_gif(frames: list[Image.Image], out_path: Path, duration: int) -> None:
    if not frames:
        raise ValueError("No frames to encode.")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
    )


def write_godot_import_note(out_dir: Path, frame_count: int, duration_ms: int) -> None:
    fps = round(1000 / duration_ms, 3) if duration_ms > 0 else 10
    note = (
        "# Godot import note\n\n"
        "- Import `sprite-strip.png` or the PNG files under `frames/`.\n"
        "- For `AnimatedSprite2D`, create a `SpriteFrames` resource and add frames in file order.\n"
        f"- Suggested FPS: `{fps}` for `{frame_count}` frames.\n"
        "- Keep one origin/anchor for the whole animation. The frames preserve source-canvas motion.\n"
    )
    (out_dir / "godot-import.md").write_text(note, encoding="utf-8")


def cmd_convert(args: argparse.Namespace) -> None:
    indices = load_indices(args.frame_indices)
    frame_paths = collect_frames(args.frames_dir, args.frame_glob, indices)
    out_dir = args.output_dir
    frames_dir = out_dir / "frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    key_color = parse_color(args.key_color)
    source_sizes: set[tuple[int, int]] = set()
    output_frames: list[Image.Image] = []
    frame_meta: list[dict[str, object]] = []

    for output_index, frame_path in enumerate(frame_paths, start=1):
        source = Image.open(frame_path).convert("RGBA")
        source_sizes.add(source.size)
        cleaned = remove_key_color(
            source,
            key_color=key_color,
            tolerance=args.tolerance,
            edge_feather=args.edge_feather,
            despill=args.despill,
        )
        fitted, scale, paste = fit_full_canvas(cleaned, (args.cell_width, args.cell_height))
        label = f"frame-{output_index:03d}.png"
        fitted.save(frames_dir / label)
        bbox = alpha_bbox(fitted)
        output_frames.append(fitted)
        frame_meta.append(
            {
                "source": str(frame_path),
                "output": f"frames/{label}",
                "source_size": list(source.size),
                "output_size": [args.cell_width, args.cell_height],
                "canvas_scale": scale,
                "canvas_paste": list(paste),
                "alpha_bbox": bbox,
                "edge_touch": bbox_touches_edge(bbox, args.cell_width, args.cell_height, args.edge_touch_margin),
            }
        )

    if len(source_sizes) > 1 and args.reject_mixed_source_sizes:
        raise ValueError(f"Input frames have mixed source sizes: {sorted(source_sizes)}.")

    compose_sheet(output_frames, len(output_frames), (args.cell_width, args.cell_height)).save(
        out_dir / "sprite-strip.png"
    )
    compose_sheet(output_frames, args.sheet_cols, (args.cell_width, args.cell_height)).save(
        out_dir / "sprite-sheet.png"
    )
    make_checker_preview(output_frames, args.sheet_cols, (args.cell_width, args.cell_height)).save(
        out_dir / "checker-preview.png"
    )
    save_transparent_gif(output_frames, out_dir / "animation.gif", args.duration)
    write_godot_import_note(out_dir, len(output_frames), args.duration)

    manifest = {
        "version": "1.1",
        "pipeline": "video_motion",
        "motion_source": "selected_full_canvas_frames",
        "frames_dir": str(args.frames_dir),
        "frame_glob": args.frame_glob,
        "frame_indices": indices,
        "key_color": f"#{key_color[0]:02x}{key_color[1]:02x}{key_color[2]:02x}",
        "tolerance": args.tolerance,
        "edge_feather": args.edge_feather,
        "despill": args.despill,
        "cell_width": args.cell_width,
        "cell_height": args.cell_height,
        "duration": args.duration,
        "sheet_cols": args.sheet_cols,
        "preserve_source_canvas": True,
        "frame_count": len(output_frames),
        "edge_touch_frames": [
            index + 1 for index, item in enumerate(frame_meta) if bool(item.get("edge_touch"))
        ],
        "frames": frame_meta,
        "outputs": {
            "frames": "frames/",
            "strip": "sprite-strip.png",
            "sheet": "sprite-sheet.png",
            "gif": "animation.gif",
            "checker_preview": "checker-preview.png",
            "godot_note": "godot-import.md",
        },
    }
    if args.reject_edge_touch and manifest["edge_touch_frames"]:
        raise ValueError(f"Frames touch the cell edge: {manifest['edge_touch_frames']}")
    (out_dir / "sprite-motion-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(str(out_dir.resolve()))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--frame-glob", default="*.png")
    parser.add_argument("--frame-indices", type=Path, help="JSON list of zero-based source frame indices to keep.")
    parser.add_argument("--key-color", default="#00ff00", help="Chroma key color as #RRGGBB or R,G,B.")
    parser.add_argument("--tolerance", type=int, default=55)
    parser.add_argument("--edge-feather", type=int, default=24)
    parser.add_argument("--despill", action="store_true")
    parser.add_argument("--cell-width", type=int, default=256)
    parser.add_argument("--cell-height", type=int, default=256)
    parser.add_argument("--sheet-cols", type=int, default=4)
    parser.add_argument("--duration", type=int, default=80)
    parser.add_argument("--edge-touch-margin", type=int, default=0)
    parser.add_argument("--reject-edge-touch", action="store_true")
    parser.add_argument("--reject-mixed-source-sizes", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cmd_convert(args)


if __name__ == "__main__":
    main()
