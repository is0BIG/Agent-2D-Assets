#!/usr/bin/env python3
"""Copy selected source frames into a compact ordered folder."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def cmd_select(args: argparse.Namespace) -> None:
    frames = sorted(args.frames_dir.glob(args.frame_glob), key=natural_key)
    if not frames:
        raise FileNotFoundError(f"No frames matched {args.frames_dir / args.frame_glob}.")
    indices = json.loads(args.frame_indices.read_text(encoding="utf-8"))
    if isinstance(indices, dict):
        indices = indices.get("frames") or indices.get("indices")
    if not isinstance(indices, list):
        raise ValueError("Frame index file must be a list or an object with frames/indices.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for output_index, source_index in enumerate(indices, start=1):
        source_index = int(source_index)
        if source_index < 0 or source_index >= len(frames):
            raise IndexError(f"Frame index out of range: {source_index}")
        target = args.output_dir / f"selected-{output_index:03d}{frames[source_index].suffix.lower()}"
        shutil.copy2(frames[source_index], target)
        copied.append({"source_index": source_index, "source": str(frames[source_index]), "output": str(target)})
    (args.output_dir / "selected-frames.json").write_text(json.dumps({"frames": copied}, indent=2), encoding="utf-8")
    print(str(args.output_dir.resolve()))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-dir", required=True, type=Path)
    parser.add_argument("--frame-indices", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--frame-glob", default="*.png")
    return parser


def main() -> None:
    cmd_select(build_parser().parse_args())


if __name__ == "__main__":
    main()
