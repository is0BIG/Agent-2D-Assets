# Godot Minimal Demo

This is a tiny Godot 4 demo for checking the engine handoff path:

- one player
- one small map area
- keyboard movement
- collision against simple walls
- idle / walk animation playback

It intentionally uses small SVG placeholder textures so the demo stays lightweight. Replace `assets/player.svg` with a generated sprite sheet when testing real `$generate2dsprite` output.

## Run

1. Open Godot 4.
2. Import this folder as a project.
3. Run `scenes/Main.tscn`.

Controls:

- Arrow keys: move
- Stop moving: idle animation

## Files

- `project.godot`: Godot project settings.
- `scenes/Main.tscn`: minimal playable scene.
- `scripts/player.gd`: movement and animation switching.
- `assets/player.svg`: placeholder player texture.
- `assets/floor.svg`: placeholder floor texture.
