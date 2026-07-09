# Unity Minimal Demo

This is a tiny Unity 2D handoff demo scaffold. It keeps the repository lightweight while providing the runtime script needed to test generated sprite sheets.

## Setup

1. Open Unity 2022.3 LTS or newer.
2. Create a new 2D project.
3. Copy this folder's `Assets` directory into the Unity project.
4. Create a scene with:
   - a `Player` GameObject with `SpriteRenderer`, `Rigidbody2D`, `BoxCollider2D`, and `PlayerController2D`.
   - a few wall GameObjects with `BoxCollider2D`.
   - an `Animator` with `Idle` and `Walk` states, or leave the animator empty and use the script for movement only.
5. Replace the placeholder sprite with output from `$generate2dsprite`.

Controls:

- Arrow keys / WASD: move
- Stop moving: idle animation parameter

## Animator Parameters

The script sets:

- `Speed` as a float
- `MoveX` as a float
- `MoveY` as a float

Use `Speed > 0.01` to transition from idle to walk.

