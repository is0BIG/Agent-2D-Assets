# Changelog

## 0.3.0-local - 2026-07-09

- Added `generate2daudio` for Codex-oriented 2D game audio assets.
- Added deterministic WAV SFX synthesis for UI packs, platformer sounds, and fireball-style spell bundles.
- Added local audio processing for trim, fade, normalize, loop flags, and metadata export.
- Added WAV analysis metadata for duration, peak, RMS, clipping samples, and loop state.
- Added audio workflow tests and a Chinese audio usage guide.

## 0.2.0-local - 2026-07-09

- Added configurable chroma key cleanup with `--key-color`, `--tolerance`, `--edge-feather`, and `--despill`.
- Added generated image import tooling for Codex image outputs.
- Added a simple image provider CLI with `local_file` and `codex_generated` providers.
- Added optional APNG and lossless animated WebP exports.
- Added sprite QC HTML report generation.
- Added processor regression tests.
- Added troubleshooting and Chinese usage documentation.
- Added minimal Godot and Unity demo projects.
- Added GitHub Actions CI.

## 0.1.0

- Initial public skill package with `generate2dsprite` and `generate2dmap`.
