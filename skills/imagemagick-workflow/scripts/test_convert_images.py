#!/usr/bin/env python3
"""Integration tests for convert_images.py.

Requires ImageMagick's `identify` and either `magick` or `convert` on PATH.
Run with: python3 scripts/test_convert_images.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("convert_images.py")


class ConvertImagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.magick = "magick" if shutil_which("magick") else "convert"
        if not shutil_which(cls.magick) or not shutil_which("identify"):
            raise unittest.SkipTest("ImageMagick magick/convert and identify are required")

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="imagemagick-skill-test-")
        self.root = Path(self.temp.name)
        self.input = self.root / "input"
        self.output = self.root / "output"
        self.input.mkdir()
        self.svg = self.input / "logo.svg"
        self.svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="80">'
            '<rect width="120" height="80" fill="#28c7a3"/></svg>\n',
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_tool(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def identify(self, path: Path) -> str:
        result = subprocess.run(
            ["identify", "-format", "%m|%wx%h|%[channels]", "--", str(path)],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout

    def test_svg_to_png_succeeds_and_verifies_output(self) -> None:
        result = self.run_tool(self.input, self.output, "--format", "png")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.output / "logo.png"
        self.assertTrue(output.is_file())
        self.assertRegex(self.identify(output), r"^PNG\|120x80\|(?:srgb|srgba)$")
        self.assertIn("Completed 1 file(s)", result.stdout)

    def test_resize_is_bounded_and_does_not_upscale(self) -> None:
        result = self.run_tool(
            self.input, self.output, "--format", "png", "--max-width", "60", "--max-height", "60"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PNG|60x40", self.identify(self.output / "logo.png"))

        second_input = self.root / "small-input"
        second_input.mkdir()
        small = second_input / "small.svg"
        small.write_text(self.svg.read_text(encoding="utf-8"), encoding="utf-8")
        second_output = self.root / "small-output"
        result = self.run_tool(second_input, second_output, "--format", "png", "--max-width", "240")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PNG|120x80", self.identify(second_output / "small.png"))

    def test_jpeg_quality_and_metadata_flag_succeed(self) -> None:
        result = self.run_tool(
            self.input,
            self.output,
            "--format",
            "jpg",
            "--quality",
            "82",
            "--strip-metadata",
            "--background",
            "white",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("JPEG|120x80", self.identify(self.output / "logo.jpg"))

    def test_original_is_never_modified(self) -> None:
        before = self.svg.read_bytes()
        result = self.run_tool(self.input, self.output, "--format", "png")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg.read_bytes(), before)

    def test_same_input_and_output_directory_is_rejected(self) -> None:
        result = self.run_tool(self.input, self.input, "--format", "png")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output directory must differ", result.stderr)

    def test_existing_output_is_not_overwritten(self) -> None:
        self.output.mkdir()
        existing = self.output / "logo.png"
        existing.write_bytes(b"sentinel")
        result = self.run_tool(self.input, self.output, "--format", "png")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(existing.read_bytes(), b"sentinel")
        self.assertIn("SKIP existing output", result.stderr)

    def test_unsupported_files_are_ignored(self) -> None:
        (self.input / "notes.txt").write_text("not an image", encoding="utf-8")
        result = self.run_tool(self.input, self.output, "--format", "png")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(p.name for p in self.output.iterdir()), ["logo.png"])

    def test_no_supported_inputs_is_rejected(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        result = self.run_tool(empty, self.output, "--format", "png")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no supported image files", result.stderr)

    def test_invalid_quality_is_rejected_by_argument_parser(self) -> None:
        result = self.run_tool(self.input, self.output, "--format", "jpg", "--quality", "101")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("between 1 and 100", result.stderr)

    def test_corrupt_input_is_reported_without_success_claim(self) -> None:
        corrupt = self.input / "broken.png"
        corrupt.write_bytes(b"not-a-valid-image")
        result = self.run_tool(self.input, self.output, "--format", "png")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Completed with", result.stderr)
        self.assertFalse((self.output / "broken.png").exists())
        self.assertTrue((self.output / "logo.png").exists())


def shutil_which(name: str) -> str | None:
    """Small local wrapper that keeps the test file dependency-free."""
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


if __name__ == "__main__":
    unittest.main(verbosity=2)
