import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_SCRIPTS = ROOT / "skills" / "generate2daudio" / "scripts"
sys.path.insert(0, str(AUDIO_SCRIPTS))

import analyze_audio
import process_audio
import synthesize_sfx
from audio_utils import read_wav_mono, write_wav_mono16


class AudioWorkflowTests(unittest.TestCase):
    def test_synthesize_single_sound_writes_wav_and_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pickup.wav"
            synthesize_sfx.main(["--sound", "pickup", "--output", str(output)])

            self.assertTrue(output.exists())
            analysis_path = output.with_suffix(".analysis.json")
            self.assertTrue(analysis_path.exists())

            data = json.loads(analysis_path.read_text(encoding="utf-8"))
            self.assertEqual(data["sound"], "pickup")
            self.assertGreater(data["duration_seconds"], 0.1)
            self.assertLessEqual(data["clipping_samples"], 0)

    def test_synthesize_preset_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            synthesize_sfx.main(["--preset", "ui-pack", "--output-dir", tmp])
            manifest = Path(tmp) / "audio-pack.json"

            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["preset"], "ui-pack")
            self.assertEqual(len(data["files"]), 4)
            self.assertTrue((Path(tmp) / "confirm.wav").exists())

    def test_process_audio_trims_fades_and_normalizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "raw.wav"
            output = Path(tmp) / "clean.wav"
            sample_rate = 44100
            samples = [0.0] * 1000 + [0.25] * 3000 + [0.0] * 1000
            write_wav_mono16(source, samples, sample_rate)

            process_audio.main(
                [
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--trim-silence",
                    "--fade-in-ms",
                    "5",
                    "--fade-out-ms",
                    "5",
                    "--normalize-peak-db",
                    "-1",
                ]
            )

            processed, _, _ = read_wav_mono(output)
            self.assertLess(len(processed), len(samples))
            data = json.loads(output.with_suffix(".analysis.json").read_text(encoding="utf-8"))
            self.assertLessEqual(data["peak_dbfs"], -0.9)
            self.assertGreater(data["duration_seconds"], 0)

    def test_analyze_audio_detects_clipping(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "clip.wav"
            output = Path(tmp) / "clip.analysis.json"
            write_wav_mono16(source, [1.0, -1.0] * 100, 44100)

            analyze_audio.main(["--input", str(source), "--output", str(output)])

            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertGreater(data["clipping_samples"], 0)


if __name__ == "__main__":
    unittest.main()
