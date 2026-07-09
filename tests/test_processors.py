from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SPRITE_SCRIPT = ROOT / "skills" / "generate2dsprite" / "scripts" / "generate2dsprite.py"
PROP_SCRIPT = ROOT / "skills" / "generate2dmap" / "scripts" / "extract_prop_pack.py"
IMPORT_SCRIPT = ROOT / "skills" / "generate2dsprite" / "scripts" / "import_generated_image.py"
PROVIDER_SCRIPT = ROOT / "skills" / "generate2dsprite" / "scripts" / "image_provider.py"
QC_SCRIPT = ROOT / "skills" / "generate2dsprite" / "scripts" / "generate_qc_report.py"


def save_sprite_grid(path: Path, size: tuple[int, int] = (128, 128)) -> None:
    img = Image.new("RGBA", size, (255, 0, 255, 255))
    pixels = img.load()
    cell_w = size[0] // 2
    cell_h = size[1] // 2
    for row in range(2):
        for col in range(2):
            left = col * cell_w + 18
            top = row * cell_h + 18
            for y in range(top, min(top + 20, size[1])):
                for x in range(left, min(left + 20, size[0])):
                    pixels[x, y] = (20, 120, 255, 255)
    img.save(path)


class ProcessorTests(unittest.TestCase):
    def run_cmd(self, args: list[str], *, expect_ok: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if expect_ok and result.returncode != 0:
            self.fail(f"Command failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        if not expect_ok and result.returncode == 0:
            self.fail(f"Command unexpectedly passed:\nSTDOUT:\n{result.stdout}")
        return result

    def test_prompt_file_is_copied_into_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            prompt = tmp_path / "prompt.txt"
            out = tmp_path / "out"
            save_sprite_grid(raw)
            prompt.write_text("manual cute slime prompt", encoding="utf-8")

            self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "creature",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(out),
                    "--prompt-file",
                    str(prompt),
                    "--rows",
                    "2",
                    "--cols",
                    "2",
                ]
            )

            meta = json.loads((out / "pipeline-meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["prompt"], "manual cute slime prompt")
            self.assertEqual((out / "prompt-used.txt").read_text(encoding="utf-8"), "manual cute slime prompt")

    def test_sprite_grid_must_divide_image_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            Image.new("RGBA", (129, 128), (255, 0, 255, 255)).save(raw)

            result = self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "creature",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(tmp_path / "out"),
                    "--rows",
                    "2",
                    "--cols",
                    "2",
                ],
                expect_ok=False,
            )
            self.assertIn("not evenly divisible", result.stderr)

    def test_largest_component_discards_small_detached_noise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            out = tmp_path / "out"
            img = Image.new("RGBA", (64, 64), (255, 0, 255, 255))
            pixels = img.load()
            for y in range(20, 44):
                for x in range(20, 44):
                    pixels[x, y] = (255, 0, 0, 255)
            for y in range(4, 8):
                for x in range(4, 8):
                    pixels[x, y] = (0, 255, 0, 255)
            img.save(raw)

            self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "asset",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(out),
                    "--rows",
                    "1",
                    "--cols",
                    "1",
                    "--cell-size",
                    "64",
                    "--component-mode",
                    "largest",
                    "--fit-scale",
                    "1",
                    "--trim-border",
                    "0",
                    "--edge-clean-depth",
                    "0",
                ]
            )

            frame = Image.open(out / "idle-1.png").convert("RGBA")
            px = frame.load()
            visible_pixels = [
                px[x, y]
                for y in range(frame.height)
                for x in range(frame.width)
                if px[x, y][3] > 0
            ]
            self.assertTrue(visible_pixels)
            self.assertFalse(any(g > 180 and r < 80 for r, g, _b, _a in visible_pixels))

    def test_sprite_despill_removes_purple_fringe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            out = tmp_path / "out"
            img = Image.new("RGBA", (64, 64), (255, 0, 255, 255))
            pixels = img.load()
            for y in range(18, 46):
                for x in range(18, 46):
                    pixels[x, y] = (40, 120, 255, 255)
            fringe = (160, 70, 230, 255)
            for x in range(16, 48):
                pixels[x, 16] = fringe
                pixels[x, 47] = fringe
            for y in range(16, 48):
                pixels[16, y] = fringe
                pixels[47, y] = fringe
            img.save(raw)

            self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "asset",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(out),
                    "--rows",
                    "1",
                    "--cols",
                    "1",
                    "--cell-size",
                    "64",
                    "--tolerance",
                    "80",
                    "--edge-threshold",
                    "80",
                    "--edge-feather",
                    "80",
                    "--despill",
                    "--fit-scale",
                    "1",
                    "--trim-border",
                    "0",
                    "--edge-clean-depth",
                    "0",
                ]
            )

            frame = Image.open(out / "idle-1.png").convert("RGBA")
            px = frame.load()
            visible = [
                px[x, y]
                for y in range(frame.height)
                for x in range(frame.width)
                if px[x, y][3] > 0
            ]
            self.assertTrue(visible)
            self.assertFalse(any(r > 120 and b > 180 and g < 120 for r, g, b, _a in visible))
            meta = json.loads((out / "pipeline-meta.json").read_text(encoding="utf-8"))
            self.assertTrue(meta["despill"])
            self.assertEqual(meta["edge_feather"], 80)

    def test_prop_pack_despill_removes_purple_fringe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "props.png"
            out = tmp_path / "props"
            img = Image.new("RGBA", (64, 64), (255, 0, 255, 255))
            pixels = img.load()
            for y in range(20, 44):
                for x in range(20, 44):
                    pixels[x, y] = (40, 120, 255, 255)
            fringe = (160, 70, 230, 255)
            for x in range(18, 46):
                pixels[x, 18] = fringe
                pixels[x, 45] = fringe
            for y in range(18, 46):
                pixels[18, y] = fringe
                pixels[45, y] = fringe
            img.save(raw)

            self.run_cmd(
                [
                    str(PROP_SCRIPT),
                    "--input",
                    str(raw),
                    "--rows",
                    "1",
                    "--cols",
                    "1",
                    "--output-dir",
                    str(out),
                    "--labels",
                    "blue-prop",
                    "--tolerance",
                    "80",
                    "--edge-threshold",
                    "80",
                    "--edge-feather",
                    "80",
                    "--despill",
                    "--trim-border",
                    "0",
                    "--edge-clean-depth",
                    "0",
                    "--component-mode",
                    "all",
                ]
            )

            prop = Image.open(out / "blue-prop" / "prop.png").convert("RGBA")
            px = prop.load()
            visible = [
                px[x, y]
                for y in range(prop.height)
                for x in range(prop.width)
                if px[x, y][3] > 0
            ]
            self.assertTrue(visible)
            self.assertFalse(any(r > 120 and b > 180 and g < 120 for r, g, b, _a in visible))
            manifest = json.loads((out / "prop-pack.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["despill"])
            self.assertEqual(manifest["edge_feather"], 80)

    def test_transparent_sheet_and_gif_are_exported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            out = tmp_path / "out"
            img = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
            pixels = img.load()
            for index, (row, col) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
                left = col * 64 + 18
                top = row * 64 + 18
                for y in range(top, top + 16 + index):
                    for x in range(left, left + 18 + index):
                        pixels[x, y] = (20 + index * 40, 120, 255, 255)
            img.save(raw)

            self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "creature",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(out),
                    "--rows",
                    "2",
                    "--cols",
                    "2",
                ]
            )

            sheet = Image.open(out / "sheet-transparent.png").convert("RGBA")
            self.assertEqual(sheet.mode, "RGBA")
            self.assertEqual(sheet.getpixel((0, 0))[3], 0)
            with Image.open(out / "animation.gif") as gif:
                self.assertEqual(getattr(gif, "n_frames", 1), 4)
                self.assertIn("transparency", gif.info)

    def test_player_sheet_exports_direction_strips_and_gifs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "player.png"
            out = tmp_path / "out"
            img = Image.new("RGBA", (160, 160), (255, 0, 255, 255))
            pixels = img.load()
            for row in range(4):
                for col in range(4):
                    left = col * 40 + 14
                    top = row * 40 + 10
                    for y in range(top, top + 18):
                        for x in range(left, left + 12):
                            pixels[x, y] = (40 + row * 40, 80 + col * 20, 220, 255)
            img.save(raw)

            self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "player",
                    "--mode",
                    "player_sheet",
                    "--output-dir",
                    str(out),
                    "--trim-border",
                    "0",
                    "--edge-clean-depth",
                    "0",
                ]
            )

            for direction in ("down", "left", "right", "up"):
                self.assertTrue((out / f"{direction}-strip.png").exists())
                self.assertTrue((out / f"{direction}.gif").exists())
            meta = json.loads((out / "pipeline-meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["rows"], 4)
            self.assertEqual(meta["cols"], 4)

    def test_reject_edge_touch_fails_for_boundary_pixels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            img = Image.new("RGBA", (64, 64), (255, 0, 255, 255))
            pixels = img.load()
            for y in range(16, 32):
                pixels[0, y] = (20, 120, 255, 255)
                pixels[1, y] = (20, 120, 255, 255)
            img.save(raw)

            result = self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "asset",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(tmp_path / "out"),
                    "--rows",
                    "1",
                    "--cols",
                    "1",
                    "--trim-border",
                    "0",
                    "--edge-clean-depth",
                    "0",
                    "--reject-edge-touch",
                ],
                expect_ok=False,
            )
            self.assertIn("Frames touch a cell edge", result.stderr)

    def test_import_generated_image_copies_latest_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            generated_root = tmp_path / "generated_images"
            session = generated_root / "session-a"
            session.mkdir(parents=True)
            older = session / "older.png"
            newer = session / "newer.png"
            Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(older)
            Image.new("RGBA", (4, 4), (0, 255, 0, 255)).save(newer)
            os.utime(older, (1, 1))
            os.utime(newer, (2, 2))
            out = tmp_path / "run" / "raw-sheet.png"

            self.run_cmd(
                [
                    str(IMPORT_SCRIPT),
                    "--generated-root",
                    str(generated_root),
                    "--output",
                    str(out),
                ]
            )

            copied = Image.open(out).convert("RGBA")
            self.assertEqual(copied.getpixel((0, 0)), (0, 255, 0, 255))
            manifest = json.loads((out.parent / "import-generated-image.json").read_text(encoding="utf-8"))
            self.assertEqual(Path(manifest["source"]).name, "newer.png")

    def test_apng_webp_and_qc_report_are_exported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw.png"
            out = tmp_path / "out"
            save_sprite_grid(raw)

            self.run_cmd(
                [
                    str(SPRITE_SCRIPT),
                    "process",
                    "--input",
                    str(raw),
                    "--target",
                    "creature",
                    "--mode",
                    "idle",
                    "--output-dir",
                    str(out),
                    "--rows",
                    "2",
                    "--cols",
                    "2",
                    "--apng",
                    "--webp",
                ]
            )
            self.assertTrue((out / "animation.png").exists())
            self.assertTrue((out / "animation.webp").exists())

            self.run_cmd([str(QC_SCRIPT), "--input-dir", str(out)])
            report = out / "qc-report.html"
            self.assertTrue(report.exists())
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("Sprite QC Report", report_text)
            self.assertIn("edge_touch_frames", report_text)

    def test_image_provider_local_file_copies_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source.png"
            output = tmp_path / "out" / "raw-sheet.png"
            Image.new("RGBA", (4, 4), (10, 20, 30, 255)).save(source)

            self.run_cmd(
                [
                    str(PROVIDER_SCRIPT),
                    "--provider",
                    "local_file",
                    "--source",
                    str(source),
                    "--output",
                    str(output),
                ]
            )

            copied = Image.open(output).convert("RGBA")
            self.assertEqual(copied.getpixel((0, 0)), (10, 20, 30, 255))
            manifest = json.loads((output.parent / "image-provider.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["provider"], "local_file")

    def test_prop_pack_grid_must_divide_image_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "props.png"
            Image.new("RGBA", (65, 64), (255, 0, 255, 255)).save(raw)

            result = self.run_cmd(
                [
                    str(PROP_SCRIPT),
                    "--input",
                    str(raw),
                    "--rows",
                    "2",
                    "--cols",
                    "2",
                    "--output-dir",
                    str(tmp_path / "props"),
                ],
                expect_ok=False,
            )
            self.assertIn("not evenly divisible", result.stderr)


if __name__ == "__main__":
    unittest.main()
