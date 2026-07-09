#!/usr/bin/env python3
"""Trim, fade, normalize, and annotate mono/stereo WAV input."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from audio_utils import analyze_samples, fade, normalize_peak, read_wav_mono, trim_silence, write_json, write_wav_mono16


def soften_loop_boundary(samples: List[float], sample_rate: int, crossfade_ms: float) -> List[float]:
    out = list(samples)
    count = min(len(out) // 2, int(sample_rate * crossfade_ms / 1000.0))
    if count <= 1:
        return out
    for i in range(count):
        t = i / (count - 1)
        blended = out[i] * t + out[-count + i] * (1.0 - t)
        out[i] = blended
        out[-count + i] = blended
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process a WAV file for game-audio handoff.")
    parser.add_argument("--input", required=True, help="Source WAV file.")
    parser.add_argument("--output", required=True, help="Processed WAV file.")
    parser.add_argument("--trim-silence", action="store_true")
    parser.add_argument("--silence-threshold-db", type=float, default=-55.0)
    parser.add_argument("--fade-in-ms", type=float, default=0.0)
    parser.add_argument("--fade-out-ms", type=float, default=30.0)
    parser.add_argument("--normalize-peak-db", type=float, default=-1.0)
    parser.add_argument("--loop", choices=["none", "seamless", "crossfade"], default="none")
    parser.add_argument("--crossfade-ms", type=float, default=20.0)
    parser.add_argument("--metadata", help="Metadata JSON output path. Defaults to output.analysis.json.")
    return parser


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    samples, sample_rate, source_channels = read_wav_mono(args.input)

    if args.trim_silence:
        samples = trim_silence(samples, args.silence_threshold_db, sample_rate=sample_rate)
    samples = fade(samples, sample_rate, args.fade_in_ms, args.fade_out_ms)
    if args.loop == "crossfade":
        samples = soften_loop_boundary(samples, sample_rate, args.crossfade_ms)
    samples = normalize_peak(samples, args.normalize_peak_db)

    output = Path(args.output)
    write_wav_mono16(output, samples, sample_rate)

    metadata = analyze_samples(samples, sample_rate, source=str(output), channels=1, loop=args.loop != "none")
    metadata.update(
        {
            "input": str(args.input),
            "output": str(output),
            "source_channels": source_channels,
            "processing": {
                "trim_silence": args.trim_silence,
                "silence_threshold_db": args.silence_threshold_db,
                "fade_in_ms": args.fade_in_ms,
                "fade_out_ms": args.fade_out_ms,
                "normalize_peak_db": args.normalize_peak_db,
                "loop": args.loop,
                "crossfade_ms": args.crossfade_ms,
            },
        }
    )
    write_json(args.metadata or output.with_suffix(".analysis.json"), metadata)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
