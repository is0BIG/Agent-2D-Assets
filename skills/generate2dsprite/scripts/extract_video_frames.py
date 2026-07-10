#!/usr/bin/env python3
"""Extract full-canvas PNG frames from a source video with ffmpeg."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def cmd_extract(args: argparse.Namespace) -> None:
    if shutil.which(args.ffmpeg) is None:
        raise FileNotFoundError(
            f"Could not find '{args.ffmpeg}'. Install ffmpeg or pass --ffmpeg with an absolute path."
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pattern = args.output_dir / args.pattern
    command = [args.ffmpeg, "-y", "-i", str(args.input)]
    if args.fps:
        command.extend(["-vf", f"fps={args.fps}"])
    command.append(str(pattern))
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg frame extraction failed.")
    frames = sorted(args.output_dir.glob(args.pattern.replace("%04d", "*")))
    manifest = {
        "input": str(args.input),
        "output_dir": str(args.output_dir),
        "pattern": args.pattern,
        "fps": args.fps,
        "frame_count": len(frames),
        "preserve_source_canvas": True,
        "note": "Frames are extracted without crop. Keep full canvas for animation alignment.",
    }
    (args.output_dir / "extract-video-frames.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(str(args.output_dir.resolve()))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--pattern", default="frame-%04d.png")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    return parser


def main() -> None:
    cmd_extract(build_parser().parse_args())


if __name__ == "__main__":
    main()
