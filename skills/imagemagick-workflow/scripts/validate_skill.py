#!/usr/bin/env python3
"""Minimal CI validator for the ImageMagick custom skill package."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
CONVERTER = ROOT / "scripts" / "convert_images.py"
TESTS = ROOT / "scripts" / "test_convert_images.py"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not SKILL.is_file():
        fail("SKILL.md is missing")
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must begin with YAML frontmatter")
    frontmatter = text.split("---\n", 2)
    if len(frontmatter) < 3:
        fail("SKILL.md has an unterminated YAML frontmatter block")
    metadata = frontmatter[1]
    name = re.search(r"^name:\s*([^\n]+)$", metadata, re.MULTILINE)
    description = re.search(r"^description:\s*(.+)$", metadata, re.MULTILINE)
    if not name or name.group(1).strip() != "imagemagick-workflow":
        fail("frontmatter name must be imagemagick-workflow")
    if not description or len(description.group(1).strip()) < 40:
        fail("frontmatter description is missing or too short")
    for required in (CONVERTER, TESTS):
        if not required.is_file():
            fail(f"required file is missing: {required.relative_to(ROOT)}")
    required_sections = ("Operating procedure", "Safety and quality rules", "Verification checklist")
    for section in required_sections:
        if f"## {section}" not in text:
            fail(f"SKILL.md is missing section: {section}")
    print("Skill structure and metadata are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
