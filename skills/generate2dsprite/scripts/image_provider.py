#!/usr/bin/env python3
"""Resolve raw image inputs from simple providers into a local file."""

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


def newest_file(root: Path, pattern: str) -> Path:
    if not root.exists():
        raise FileNotFoundError(f"Provider root not found: {root}")
    candidates = [path for path in root.rglob(pattern) if path.is_file()]
    if not candidates:
        raise FileNotFoundError(f"No files matched {pattern!r} under {root}")
    candidates.sort(key=lambda path: (path.stat().st_mtime, str(path)), reverse=True)
    return candidates[0]


def copy_source(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, choices=["local_file", "codex_generated"])
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source", type=Path, help="Required for local_file.")
    parser.add_argument("--generated-root", type=Path, default=default_generated_root())
    parser.add_argument("--session")
    parser.add_argument("--pattern", default="*.png")
    parser.add_argument("--manifest", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.provider == "local_file":
        if not args.source:
            raise ValueError("--source is required for provider=local_file.")
        source = args.source
        if not source.exists():
            raise FileNotFoundError(f"Local source not found: {source}")
    else:
        root = args.generated_root / args.session if args.session else args.generated_root
        source = newest_file(root, args.pattern)

    copy_source(source, args.output)
    manifest_path = args.manifest or (args.output.parent / "image-provider.json")
    manifest = {
        "provider": args.provider,
        "source": str(source),
        "output": str(args.output),
        "generated_root": str(args.generated_root),
        "session": args.session or "",
        "pattern": args.pattern,
        "resolved_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(str(args.output.resolve()))


if __name__ == "__main__":
    main()
