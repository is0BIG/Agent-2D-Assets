#!/usr/bin/env python3
"""Generate deterministic mono WAV game SFX and pack manifests."""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Callable, Dict, List

from audio_utils import DEFAULT_SAMPLE_RATE, analyze_samples, fade, normalize_peak, slugify, write_json, write_wav_mono16


PRESETS = {
    "ui-pack": ["click", "confirm", "cancel", "error"],
    "fireball-pack": ["spell-cast", "spell-loop", "spell-hit"],
    "platformer-pack": ["jump", "land", "pickup", "hit", "powerup"],
}


def envelope(index: int, total: int, attack: float = 0.02, release: float = 0.35) -> float:
    if total <= 1:
        return 0.0
    position = index / (total - 1)
    attack_gain = min(1.0, position / max(0.0001, attack))
    release_gain = max(0.0, (1.0 - position) / max(0.0001, release))
    return min(attack_gain, release_gain, 1.0)


def tone(duration: float, sample_rate: int, freq_start: float, freq_end: float | None = None, wave_shape: str = "sine") -> List[float]:
    total = max(1, int(duration * sample_rate))
    freq_end = freq_start if freq_end is None else freq_end
    phase = 0.0
    out: List[float] = []
    for i in range(total):
        t = i / max(1, total - 1)
        freq = freq_start + (freq_end - freq_start) * t
        phase += 2.0 * math.pi * freq / sample_rate
        if wave_shape == "square":
            value = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave_shape == "triangle":
            value = (2.0 / math.pi) * math.asin(math.sin(phase))
        else:
            value = math.sin(phase)
        out.append(value)
    return out


def mix(layers: List[List[float]]) -> List[float]:
    length = max((len(layer) for layer in layers), default=0)
    out = [0.0] * length
    for layer in layers:
        for i, value in enumerate(layer):
            out[i] += value
    return [max(-1.0, min(1.0, value)) for value in out]


def add_at(base: List[float], layer: List[float], offset_seconds: float, sample_rate: int, gain: float = 1.0) -> List[float]:
    offset = max(0, int(offset_seconds * sample_rate))
    needed = offset + len(layer)
    if len(base) < needed:
        base.extend([0.0] * (needed - len(base)))
    for i, value in enumerate(layer):
        base[offset + i] += value * gain
    return base


def shaped(samples: List[float], sample_rate: int, gain: float = 0.7, attack: float = 0.02, release: float = 0.35) -> List[float]:
    total = len(samples)
    return [sample * gain * envelope(i, total, attack, release) for i, sample in enumerate(samples)]


def noise(duration: float, sample_rate: int, rng: random.Random) -> List[float]:
    return [rng.uniform(-1.0, 1.0) for _ in range(max(1, int(duration * sample_rate)))]


def synth_click(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    return fade(shaped(tone(duration or 0.08, sample_rate, 1200, 1800, "triangle"), sample_rate, 0.55, 0.01, 0.12), sample_rate, 1, 20)


def synth_confirm(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    base: List[float] = []
    add_at(base, shaped(tone(0.09, sample_rate, 660), sample_rate, 0.45, 0.02, 0.18), 0.0, sample_rate)
    add_at(base, shaped(tone(0.13, sample_rate, 990), sample_rate, 0.42, 0.02, 0.22), 0.08, sample_rate)
    return fade(base, sample_rate, 2, 25)


def synth_cancel(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    return fade(shaped(tone(duration or 0.18, sample_rate, 520, 220, "triangle"), sample_rate, 0.55, 0.01, 0.25), sample_rate, 2, 35)


def synth_error(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    base: List[float] = []
    buzz = shaped(tone(0.11, sample_rate, 170, 150, "square"), sample_rate, 0.32, 0.02, 0.22)
    add_at(base, buzz, 0.0, sample_rate)
    add_at(base, buzz, 0.13, sample_rate)
    return fade(base, sample_rate, 3, 40)


def synth_pickup(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    base: List[float] = []
    for offset, freq in [(0.00, 740), (0.07, 990), (0.14, 1480)]:
        add_at(base, shaped(tone(0.11, sample_rate, freq, freq * 1.05), sample_rate, 0.38, 0.03, 0.2), offset, sample_rate)
    return fade(base, sample_rate, 2, 35)


def synth_hit(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    thump = shaped(tone(duration or 0.18, sample_rate, 150, 70), sample_rate, 0.62, 0.005, 0.22)
    grit = shaped(noise(duration or 0.18, sample_rate, rng), sample_rate, 0.18, 0.001, 0.15)
    return fade(mix([thump, grit]), sample_rate, 1, 45)


def synth_explosion(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    length = duration or 0.85
    rumble = shaped(tone(length, sample_rate, 92, 38), sample_rate, 0.55, 0.005, 0.85)
    blast = shaped(noise(length, sample_rate, rng), sample_rate, 0.38, 0.001, 0.55)
    return fade(mix([rumble, blast]), sample_rate, 2, 80)


def synth_laser(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    main = shaped(tone(duration or 0.28, sample_rate, 1500, 330, "square"), sample_rate, 0.42, 0.01, 0.28)
    body = shaped(tone(duration or 0.28, sample_rate, 760, 220), sample_rate, 0.35, 0.01, 0.3)
    return fade(mix([main, body]), sample_rate, 1, 45)


def synth_jump(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    return fade(shaped(tone(duration or 0.22, sample_rate, 220, 720, "triangle"), sample_rate, 0.55, 0.03, 0.22), sample_rate, 2, 35)


def synth_land(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    return fade(shaped(tone(duration or 0.12, sample_rate, 120, 62), sample_rate, 0.48, 0.005, 0.18), sample_rate, 1, 35)


def synth_powerup(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    base: List[float] = []
    for step, freq in enumerate([330, 440, 660, 880]):
        add_at(base, shaped(tone(0.14, sample_rate, freq, freq * 1.15), sample_rate, 0.32, 0.02, 0.25), step * 0.08, sample_rate)
    return fade(base, sample_rate, 2, 60)


def synth_spell_cast(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    shimmer = shaped(tone(duration or 0.45, sample_rate, 360, 1240, "triangle"), sample_rate, 0.36, 0.08, 0.5)
    air = shaped(noise(duration or 0.45, sample_rate, rng), sample_rate, 0.12, 0.04, 0.45)
    return fade(mix([shimmer, air]), sample_rate, 8, 75)


def synth_spell_loop(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    length = duration or 0.75
    a = shaped(tone(length, sample_rate, 220, 220), sample_rate, 0.22, 0.08, 0.08)
    b = shaped(tone(length, sample_rate, 330, 330, "triangle"), sample_rate, 0.18, 0.08, 0.08)
    return fade(mix([a, b]), sample_rate, 10, 10)


def synth_spell_hit(sample_rate: int, rng: random.Random, duration: float | None = None) -> List[float]:
    burst = shaped(noise(duration or 0.5, sample_rate, rng), sample_rate, 0.3, 0.001, 0.45)
    core = shaped(tone(duration or 0.5, sample_rate, 480, 90), sample_rate, 0.45, 0.005, 0.5)
    return fade(mix([burst, core]), sample_rate, 2, 70)


SYNTHS: Dict[str, Callable[[int, random.Random, float | None], List[float]]] = {
    "click": synth_click,
    "confirm": synth_confirm,
    "cancel": synth_cancel,
    "error": synth_error,
    "pickup": synth_pickup,
    "hit": synth_hit,
    "explosion": synth_explosion,
    "laser": synth_laser,
    "jump": synth_jump,
    "land": synth_land,
    "powerup": synth_powerup,
    "spell-cast": synth_spell_cast,
    "spell-loop": synth_spell_loop,
    "spell-hit": synth_spell_hit,
}


def synthesize_sound(sound: str, sample_rate: int, seed: int = 7, duration: float | None = None, target_peak_db: float = -1.0) -> List[float]:
    sound = slugify(sound)
    if sound not in SYNTHS:
        raise ValueError(f"Unknown sound '{sound}'. Available: {', '.join(sorted(SYNTHS))}")
    rng = random.Random(f"{seed}:{sound}")
    return normalize_peak(SYNTHS[sound](sample_rate, rng, duration), target_peak_db)


def write_sound(sound: str, output: Path, sample_rate: int, seed: int, duration: float | None, target_peak_db: float, style: str) -> dict:
    samples = synthesize_sound(sound, sample_rate, seed, duration, target_peak_db)
    write_wav_mono16(output, samples, sample_rate)
    analysis = analyze_samples(samples, sample_rate, source=str(output), loop=sound.endswith("-loop"))
    analysis.update({"id": output.stem, "sound": sound, "style": style, "file": output.name})
    write_json(output.with_suffix(".analysis.json"), analysis)
    return analysis


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate deterministic game SFX WAV files.")
    parser.add_argument("--sound", choices=sorted(SYNTHS), help="Single sound to synthesize.")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="Pack preset to synthesize.")
    parser.add_argument("--output", help="Output WAV path for a single sound.")
    parser.add_argument("--output-dir", default="outputs/audio", help="Directory for preset output.")
    parser.add_argument("--duration", type=float, help="Override duration in seconds.")
    parser.add_argument("--sample-rate", type=int, default=DEFAULT_SAMPLE_RATE)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--style", default="arcade", help="Style tag for metadata: retro, chiptune, fantasy, sci_fi, cozy, arcade, horror.")
    parser.add_argument("--normalize-peak-db", type=float, default=-1.0)
    parser.add_argument("--manifest-name", default="audio-pack.json")
    return parser


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.sound and not args.preset:
        raise SystemExit("Choose --sound or --preset.")

    if args.sound:
        output = Path(args.output or Path(args.output_dir) / f"{slugify(args.sound)}.wav")
        write_sound(args.sound, output, args.sample_rate, args.seed, args.duration, args.normalize_peak_db, args.style)
        print(output)
        return 0

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for sound in PRESETS[args.preset]:
        path = output_dir / f"{slugify(sound)}.wav"
        entries.append(write_sound(sound, path, args.sample_rate, args.seed, args.duration, args.normalize_peak_db, args.style))

    manifest = {
        "preset": args.preset,
        "sample_rate": args.sample_rate,
        "style": args.style,
        "format": "wav",
        "channels": 1,
        "files": entries,
    }
    write_json(output_dir / args.manifest_name, manifest)
    print(output_dir / args.manifest_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
