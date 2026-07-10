# Changelog

## 1.1.0 - 2026-07-10

- Added the `generate2dsprite` 1.1 video-motion workflow for body actions such as walk, run, attack, cast, jump, hurt, death, and transformation.
- Added `extract_video_frames.py` for full-canvas ffmpeg frame extraction.
- Added `make_contact_sheet.py` for numbered frame review and semantic keyframe selection.
- Added `select_frames.py` for copying selected source frames into an ordered folder.
- Added `video_to_sprite.py` for green-screen or chroma-key frame cleanup, fixed-canvas transparent frame export, sprite strip/sheet export, GIF preview, checker preview, Godot import notes, and motion manifests.
- Updated sprite skill rules to keep the 1.0 direct-sheet workflow while preferring 1.1 video-motion for character body animation continuity.
- Updated Chinese, English, Traditional Chinese, Japanese, and Korean README files with 1.0 / 1.1 version guidance.
- Added tests that verify video-motion exports preserve source-canvas movement instead of recentering every frame.

## 1.0.0 - 2026-07-10

- Marked the existing Agent-2D-Assets workflow as the 1.0 baseline.
- The 1.0 baseline includes `generate2dsprite`, `generate2dmap`, and `generate2daudio`; committed sprite/map/audio examples; Godot / Unity minimal demos; multilingual documentation; and local processor tests.

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
