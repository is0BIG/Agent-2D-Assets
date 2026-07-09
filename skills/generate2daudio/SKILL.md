---
name: generate2daudio
description: "Generate and postprocess 2D game audio assets for Codex workflows: UI sounds, combat SFX, spell bundles, character actions, pickups, ambience loops, and engine-ready WAV metadata. Use when Codex should plan a game-audio asset pack, synthesize simple local SFX, process supplied WAV files with trim/fade/normalize options, analyze duration/peak/RMS/clipping, and export manifests for Godot, Unity, web, or raw 2D game projects."
---

# Generate2daudio

Use this skill for self-contained 2D game audio assets and audio packs.

This skill mirrors the asset workflow of `$generate2dsprite` and `$generate2dmap`: Codex plans the audio bundle, then deterministic local scripts synthesize simple SFX, process supplied WAV files, export metadata, and run QA checks.

## Parameters

Infer these from the user request:

- `asset_type`: `ui` | `combat` | `magic` | `character` | `pickup` | `ambience` | `bgm` | `pack`
- `sound`: `click` | `confirm` | `cancel` | `error` | `pickup` | `hit` | `explosion` | `laser` | `jump` | `powerup`
- `bundle`: `single` | `ui_pack` | `fireball_pack` | `platformer_pack`
- `style`: `retro` | `chiptune` | `fantasy` | `sci_fi` | `cozy` | `arcade` | `horror`
- `duration`: explicit seconds or `auto`
- `loop`: `none` | `seamless` | `crossfade`
- `engine_target`: `raw` | `Godot` | `Unity` | `Web`
- `output_format`: `wav` initially; add OGG/MP3 only when a converter is available
- `prompt`: user-facing theme or gameplay role

Read [references/audio-styles.md](references/audio-styles.md) when the style or bundle shape is unclear.

## Agent Rules

- Prefer local deterministic SFX synthesis for simple UI, combat, pickup, jump, laser, and powerup sounds.
- For music, voice, and rich ambience, plan the asset and use a provider or supplied audio file when available; do not pretend local synthesis can produce production-quality music.
- Keep SFX short and gameplay-readable. UI clicks are usually under 0.2s; pickups and jumps under 0.5s; explosions and impacts under 1.5s.
- Avoid clipping. Normalize peaks to about `-1 dBFS` unless the user asks for raw output.
- Always write metadata next to generated audio. Include sound id, duration, sample rate, peak, RMS, clipping count, and loop flag.
- For loops, add clear loop metadata. If the loop is not actually seamless, mark it as a draft.
- Do not use copyrighted music, voices, or recognizable sound effects unless the user supplies rights-cleared source audio.

## Workflow

### 1. Plan the audio pack

Choose the smallest useful deliverable:

- menu request -> `ui_pack`
- spell request -> `fireball_pack` or custom spell bundle
- platformer request -> `platformer_pack`
- one action -> `single`
- supplied audio cleanup -> process/analyze existing WAV

### 2. Generate or process audio

Use scripts:

```bash
python scripts/synthesize_sfx.py --preset ui-pack --output-dir outputs/audio/ui
```

```bash
python scripts/synthesize_sfx.py --sound pickup --output outputs/audio/pickup.wav
```

```bash
python scripts/process_audio.py --input raw.wav --output clean.wav --trim-silence --fade-in-ms 5 --fade-out-ms 30 --normalize-peak-db -1
```

### 3. Analyze and validate

Run:

```bash
python scripts/analyze_audio.py --input outputs/audio/ui/confirm.wav --output outputs/audio/ui/confirm.analysis.json
```

Check:

- duration matches gameplay use
- peak is not clipped
- RMS is not near silence
- loop metadata exists when requested
- filenames are engine-friendly

### 4. Return the bundle

For a single SFX:

- `sound.wav`
- `sound.analysis.json`

For an audio pack:

- one WAV per sound
- `audio-pack.json`
- optional per-file analysis JSON

## Defaults

- sample rate: `44100`
- channels: mono
- bit depth: 16-bit PCM WAV
- normalize peak: `-1 dBFS`
- fade out: short SFX usually 20-60ms
- file names: lowercase slugs

## Resources

- `scripts/synthesize_sfx.py`: deterministic SFX and pack synthesis
- `scripts/process_audio.py`: trim, fade, normalize, and metadata processing for WAV files
- `scripts/analyze_audio.py`: audio QA metadata
- `references/audio-styles.md`: style and bundle guidance
- `references/game-audio-contract.md`: output contract and engine handoff
