"""Small stdlib-only helpers for deterministic game SFX processing."""

from __future__ import annotations

import json
import math
import os
import re
import wave
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


DEFAULT_SAMPLE_RATE = 44100


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "sound"


def ensure_parent(path: str | os.PathLike[str]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def clamp(sample: float) -> float:
    return max(-1.0, min(1.0, float(sample)))


def db_to_amplitude(db: float) -> float:
    return 10.0 ** (db / 20.0)


def amplitude_to_db(amplitude: float) -> float:
    if amplitude <= 0:
        return float("-inf")
    return 20.0 * math.log10(amplitude)


def peak(samples: Sequence[float]) -> float:
    return max((abs(s) for s in samples), default=0.0)


def rms(samples: Sequence[float]) -> float:
    if not samples:
        return 0.0
    return math.sqrt(sum(float(s) * float(s) for s in samples) / len(samples))


def normalize_peak(samples: Sequence[float], target_db: float = -1.0) -> List[float]:
    current = peak(samples)
    if current <= 0:
        return list(samples)
    target = db_to_amplitude(target_db)
    gain = target / current
    return [clamp(s * gain) for s in samples]


def fade(samples: Sequence[float], sample_rate: int, fade_in_ms: float = 0.0, fade_out_ms: float = 0.0) -> List[float]:
    out = list(samples)
    fade_in = min(len(out), int(sample_rate * fade_in_ms / 1000.0))
    fade_out = min(len(out), int(sample_rate * fade_out_ms / 1000.0))

    if fade_in > 0:
        for i in range(fade_in):
            out[i] *= i / max(1, fade_in - 1)

    if fade_out > 0:
        start = len(out) - fade_out
        for i in range(fade_out):
            out[start + i] *= 1.0 - (i / max(1, fade_out - 1))

    return [clamp(s) for s in out]


def trim_silence(samples: Sequence[float], threshold_db: float = -55.0, pad_ms: float = 3.0, sample_rate: int = DEFAULT_SAMPLE_RATE) -> List[float]:
    if not samples:
        return []
    threshold = db_to_amplitude(threshold_db)
    first = 0
    last = len(samples) - 1

    while first < len(samples) and abs(samples[first]) < threshold:
        first += 1
    while last >= first and abs(samples[last]) < threshold:
        last -= 1

    if first >= len(samples) or last < first:
        return []

    pad = int(sample_rate * pad_ms / 1000.0)
    first = max(0, first - pad)
    last = min(len(samples) - 1, last + pad)
    return list(samples[first : last + 1])


def read_wav_mono(path: str | os.PathLike[str]) -> Tuple[List[float], int, int]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.readframes(wav.getnframes())

    if sample_width not in {1, 2, 4}:
        raise ValueError(f"Unsupported WAV sample width: {sample_width} bytes")

    samples: List[float] = []
    frame_width = sample_width * channels
    for offset in range(0, len(frames), frame_width):
        channel_values = []
        for channel in range(channels):
            start = offset + channel * sample_width
            raw = frames[start : start + sample_width]
            if sample_width == 1:
                value = (raw[0] - 128) / 128.0
            elif sample_width == 2:
                value = int.from_bytes(raw, "little", signed=True) / 32768.0
            else:
                value = int.from_bytes(raw, "little", signed=True) / 2147483648.0
            channel_values.append(value)
        samples.append(sum(channel_values) / channels)
    return samples, sample_rate, channels


def write_wav_mono16(path: str | os.PathLike[str], samples: Iterable[float], sample_rate: int = DEFAULT_SAMPLE_RATE) -> None:
    ensure_parent(path)
    pcm = bytearray()
    for sample in samples:
        value = int(round(clamp(sample) * 32767.0))
        pcm.extend(value.to_bytes(2, "little", signed=True))

    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(bytes(pcm))


def analyze_samples(samples: Sequence[float], sample_rate: int, source: str | None = None, channels: int = 1, loop: bool = False) -> dict:
    peak_value = peak(samples)
    rms_value = rms(samples)
    clipping = sum(1 for s in samples if abs(s) >= 0.999)
    return {
        "source": source,
        "sample_rate": sample_rate,
        "channels": channels,
        "sample_count": len(samples),
        "duration_seconds": round(len(samples) / sample_rate, 6) if sample_rate else 0.0,
        "peak": round(peak_value, 6),
        "peak_dbfs": None if peak_value <= 0 else round(amplitude_to_db(peak_value), 3),
        "rms": round(rms_value, 6),
        "rms_dbfs": None if rms_value <= 0 else round(amplitude_to_db(rms_value), 3),
        "clipping_samples": clipping,
        "near_silence": rms_value < db_to_amplitude(-55.0),
        "loop": bool(loop),
    }


def read_json(path: str | os.PathLike[str]) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | os.PathLike[str], data: dict) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
