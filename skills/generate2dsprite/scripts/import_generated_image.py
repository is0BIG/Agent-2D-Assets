#!/usr/bin/env python3
"""Copy the latest built-in image_gen output into a local asset run folder."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


def default_generated_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "generated_images"
    return Path.home() / ".codex" / "generated_images"


def find_candidates(root: Path, pattern: str, session: str | None) -> list[Path]:
    search_root = root / session if session else root
    if not search_root.exists():
        raise FileNotFoundError(f"Generated image root not found: {search_root}")
    candidates = [path for path in search_root.rglob(pattern) if path.is_file()]
    candidates.sort(key=lambda path: (path.stat().st_mtime, str(path)), reverse=True)
    return candidates


def resolve_output_path(output: Path, source: Path, default_name: str) -> Path:
    if output.suffix:
        return output
    filename = default_name or source.name
    return output / filename


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Destination file or directory.")
    parser.add_argument("--generated-root", type=Path, default=default_generated_root())
    parser.add_argument("--session", help="Optional generated_images session folder name.")
    parser.add_argument("--pattern", default="*.png")
    parser.add_argument("--latest-index", type=int, default=0, help="0 means newest, 1 means second newest.")
    parser.add_argument("--default-name", default="raw-sheet.png")
    parser.add_argument("--manifest", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.latest_index < 0:
        raise ValueError("--latest-index must be zero or greater.")

    candidates = find_candidates(args.generated_root, args.pattern, args.session)
    if not candidates:
        raise FileNotFoundError(
            f"No generated images matched pattern {args.pattern!r} under {args.generated_root}."
        )
    if args.latest_index >= len(candidates):
        raise IndexError(f"--latest-index {args.latest_index} requested, but only {len(candidates)} files matched.")

    source = candidates[args.latest_index]
    output = resolve_output_path(args.output, source, args.default_name)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)

    manifest_path = args.manifest or (output.parent / "import-generated-image.json")
    manifest = {
        "source": str(source),
        "output": str(output),
        "generated_root": str(args.generated_root),
        "session": args.session or "",
        "pattern": args.pattern,
        "latest_index": args.latest_index,
        "copied_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(str(output.resolve()))


if __name__ == "__main__":
    main()
