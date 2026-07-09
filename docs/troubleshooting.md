# Troubleshooting

This guide covers the most common local processor failures.

## image_gen finished, but no local PNG was processed

Built-in image generation saves files under:

```text
$CODEX_HOME/generated_images
```

or, when `CODEX_HOME` is not set:

```text
~/.codex/generated_images
```

Copy the newest generated PNG into a local run folder:

```bash
python skills/generate2dsprite/scripts/import_generated_image.py \
  --output outputs/my-run/raw-sheet.png
```

Then process it:

```bash
python skills/generate2dsprite/scripts/generate2dsprite.py process \
  --input outputs/my-run/raw-sheet.png \
  --target creature \
  --mode idle \
  --output-dir outputs/my-run/processed \
  --rows 2 \
  --cols 2
```

If the newest file is not the one you want, use `--latest-index 1`, `--latest-index 2`, or `--session <folder-name>`.

## Purple or magenta fringe remains after cleanup

Use soft edge cleanup and despill:

```bash
python skills/generate2dsprite/scripts/generate2dsprite.py process \
  --input raw-sheet.png \
  --target creature \
  --mode idle \
  --output-dir out \
  --rows 2 \
  --cols 2 \
  --tolerance 80 \
  --edge-threshold 80 \
  --edge-feather 80 \
  --despill
```

If the asset itself contains purple or pink, lower `--tolerance` and `--edge-feather`.

## The script says the image is not evenly divisible by the grid

The processor requires equal-sized cells. A 2x2 sheet must have width and height divisible by 2. A 4x4 sheet must have width and height divisible by 4.

Fix by padding, cropping, resizing, or regenerating the raw sheet.

## `edge_touch_frames` is not empty

At least one subject touches a cell boundary. Prefer regenerating the raw sheet with stricter wording:

```text
The subject fills only the central 60% to 70% of each cell, with generous solid magenta margin on all four sides. Nothing may touch or cross a cell edge.
```

For local postprocessing, you can also reduce `--fit-scale`, but this cannot restore pixels that were clipped in the raw image.

## GIF preview shows a magenta background

GIF transparency is palette-index based. Some viewers display the transparent index as magenta. Check `sheet-transparent.png` or individual frame PNG files first. If PNG outputs are transparent, the asset is usually usable.

## Prop pack extraction keeps tiny noise

Use largest-component mode when each cell should contain exactly one prop:

```bash
python skills/generate2dmap/scripts/extract_prop_pack.py \
  --input prop-pack.png \
  --rows 3 \
  --cols 3 \
  --output-dir props \
  --component-mode largest
```

Use `--component-mode all` only for effects or intentionally detached pieces.
