#!/usr/bin/env python3
"""Generate a small HTML QC report for a processed sprite output folder."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def link(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_dir = args.input_dir
    metadata_path = input_dir / "pipeline-meta.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing pipeline metadata: {metadata_path}")
    meta = read_json(metadata_path)
    output = args.output or (input_dir / "qc-report.html")

    rows = []
    for index, label in enumerate(meta.get("frame_labels", [])):
        frame_path = input_dir / f"{label}.png"
        info = meta.get("frames", [{}])[index] if index < len(meta.get("frames", [])) else {}
        rows.append(
            "<tr>"
            f"<td>{index + 1}</td>"
            f"<td>{html.escape(str(label))}</td>"
            f"<td><img class='frame' src='{html.escape(link(frame_path, output.parent))}' alt='{html.escape(str(label))}'></td>"
            f"<td>{html.escape(json.dumps(info.get('crop_bbox'), ensure_ascii=False))}</td>"
            f"<td>{html.escape(json.dumps(info.get('output_size'), ensure_ascii=False))}</td>"
            f"<td>{html.escape(str(info.get('edge_touch', False)))}</td>"
            "</tr>"
        )

    assets = []
    for name in ("raw-sheet.png", "raw-sheet-clean.png", "sheet-transparent.png", "animation.gif", "animation.png", "animation.webp"):
        path = input_dir / name
        if path.exists():
            assets.append(f"<li><a href='{html.escape(link(path, output.parent))}'>{html.escape(name)}</a></li>")

    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sprite QC Report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 24px; color: #1f2933; }}
    code, pre {{ background: #f4f6f8; padding: 2px 4px; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
    th, td {{ border: 1px solid #d8dee4; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f6f8fa; }}
    .frame {{ width: 96px; height: 96px; object-fit: contain; background: repeating-conic-gradient(#ddd 0% 25%, #fff 0% 50%) 50% / 16px 16px; }}
    .warn {{ color: #b42318; font-weight: 700; }}
  </style>
</head>
<body>
  <h1>Sprite QC Report</h1>
  <p><strong>Target:</strong> {html.escape(str(meta.get("target", "")))} · <strong>Mode:</strong> {html.escape(str(meta.get("mode", "")))}</p>
  <p><strong>Grid:</strong> {html.escape(str(meta.get("rows", "")))} x {html.escape(str(meta.get("cols", "")))} · <strong>Cell:</strong> {html.escape(str(meta.get("cell_size", "")))}</p>
  <p><strong>Edge touch frames:</strong> <span class='{"warn" if meta.get("edge_touch_frames") else ""}'>{html.escape(json.dumps(meta.get("edge_touch_frames", [])))}</span></p>
  <h2>Assets</h2>
  <ul>{''.join(assets)}</ul>
  <h2>Frames</h2>
  <table>
    <thead><tr><th>#</th><th>Label</th><th>Preview</th><th>Crop bbox</th><th>Output size</th><th>Edge touch</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <h2>Metadata</h2>
  <pre>{html.escape(json.dumps(meta, indent=2, ensure_ascii=False))}</pre>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    print(str(output.resolve()))


if __name__ == "__main__":
    main()
