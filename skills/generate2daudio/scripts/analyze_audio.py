#!/usr/bin/env python3
"""Analyze WAV files and write QA metadata."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from audio_utils import analyze_samples, read_wav_mono, write_json


def analyze_path(path: Path) -> dict:
    samples, sample_rate, channels = read_wav_mono(path)
    data = analyze_samples(samples, sample_rate, source=str(path), channels=channels)
    data["file"] = path.name
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a WAV file or directory of WAV files.")
    parser.add_argument("--input", required=True, help="Input WAV path or directory.")
    parser.add_argument("--output", help="Output JSON path.")
    return parser


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)

    if input_path.is_dir():
        files = sorted(input_path.glob("*.wav"))
        result = {"files": [analyze_path(path) for path in files]}
        default_output = input_path / "analysis.json"
    else:
        result = analyze_path(input_path)
        default_output = input_path.with_suffix(".analysis.json")

    output = Path(args.output) if args.output else default_output
    write_json(output, result)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
