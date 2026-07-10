#!/usr/bin/env python3
"""Create a numbered contact sheet for selecting animation frames."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def collect_frames(frames_dir: Path, pattern: str) -> list[Path]:
    frames = sorted(frames_dir.glob(pattern), key=natural_key)
    if not frames:
        raise FileNotFoundError(f"No frames matched {frames_dir / pattern}.")
    return frames


def cmd_sheet(args: argparse.Namespace) -> None:
    frames = collect_frames(args.frames_dir, args.frame_glob)
    thumbs = []
    for frame_path in frames:
        image = Image.open(frame_path).convert("RGB")
        image.thumbnail((args.thumb_width, args.thumb_height), Image.Resampling.LANCZOS)
        thumb = Image.new("RGB", (args.thumb_width, args.thumb_height + args.label_height), "white")
        thumb.paste(image, ((args.thumb_width - image.width) // 2, 0))
        thumbs.append(thumb)

    rows = (len(thumbs) + args.cols - 1) // args.cols
    sheet = Image.new(
        "RGB",
        (args.cols * args.thumb_width, rows * (args.thumb_height + args.label_height)),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, thumb in enumerate(thumbs):
        row, col = divmod(index, args.cols)
        x = col * args.thumb_width
        y = row * (args.thumb_height + args.label_height)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + args.thumb_width - 1, y + thumb.height - 1), outline=(40, 40, 40))
        draw.text((x + 6, y + args.thumb_height + 4), f"{index}: {frames[index].name}", fill=(0, 0, 0), font=font)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    manifest = {
        "frames_dir": str(args.frames_dir),
        "frame_glob": args.frame_glob,
        "output": str(args.output),
        "cols": args.cols,
        "frame_count": len(frames),
        "selection_file_hint": "Create frame_indices.json with zero-based indices, e.g. [2, 5, 8, 11].",
    }
    args.output.with_suffix(".json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(str(args.output.resolve()))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--frame-glob", default="*.png")
    parser.add_argument("--cols", type=int, default=5)
    parser.add_argument("--thumb-width", type=int, default=180)
    parser.add_argument("--thumb-height", type=int, default=140)
    parser.add_argument("--label-height", type=int, default=24)
    return parser


def main() -> None:
    cmd_sheet(build_parser().parse_args())


if __name__ == "__main__":
    main()
