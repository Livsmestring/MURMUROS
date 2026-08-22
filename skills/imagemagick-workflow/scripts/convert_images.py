#!/usr/bin/env python3
"""Safely convert a bounded set of images with ImageMagick.

The script never overwrites inputs, uses subprocess argument arrays instead of a shell,
and verifies each output with ImageMagick identify.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ALLOWED_INPUTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".gif", ".bmp", ".svg"}
ALLOWED_OUTPUTS = {"jpg", "jpeg", "png", "webp", "tif", "tiff", "gif", "bmp"}


def die(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def quality(value: str) -> int:
    parsed = positive_int(value)
    if parsed > 100:
        raise argparse.ArgumentTypeError("must be between 1 and 100")
    return parsed


def tool(name: str) -> str:
    resolved = shutil.which(name)
    if resolved:
        return resolved
    die(f"required executable not found: {name}")


def identify(identify_bin: str, path: Path) -> str:
    result = subprocess.run(
        [identify_bin, "-format", "%f | %m | %wx%h | %[channels] | %b\\n", "--", str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        die(f"verification failed for {path}: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--format", required=True, choices=sorted(ALLOWED_OUTPUTS))
    parser.add_argument("--max-width", type=positive_int, default=None)
    parser.add_argument("--max-height", type=positive_int, default=None)
    parser.add_argument("--quality", type=quality, default=None)
    parser.add_argument("--strip-metadata", action="store_true")
    parser.add_argument("--background", default=None, help="solid background color for formats without alpha")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        die(f"input directory does not exist or is not a directory: {args.input_dir}")
    if args.output_dir.resolve() == args.input_dir.resolve():
        die("output directory must differ from input directory")

    magick = tool("magick") if shutil.which("magick") else tool("convert")
    identify_bin = tool("identify")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    inputs = sorted(
        path for path in args.input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in ALLOWED_INPUTS
    )
    if not inputs:
        die(f"no supported image files found in {args.input_dir}")

    failures = 0
    for source in inputs:
        destination = args.output_dir / f"{source.stem}.{args.format}"
        if destination.exists():
            print(f"SKIP existing output: {destination}", file=sys.stderr)
            failures += 1
            continue

        command = [magick, "--", str(source)]
        if args.background:
            command += ["-background", args.background]
        if args.max_width or args.max_height:
            width = str(args.max_width or "")
            height = str(args.max_height or "")
            command += ["-resize", f"{width}x{height}>"]
        if args.strip_metadata:
            command.append("-strip")
        if args.quality is not None and args.format in {"jpg", "jpeg", "webp"}:
            command += ["-quality", str(args.quality)]
        if args.background and args.format in {"jpg", "jpeg"}:
            command += ["-alpha", "remove", "-alpha", "off"]
        command.append(str(destination))

        result = subprocess.run(command, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            print(f"FAIL {source}: {result.stderr.strip()}", file=sys.stderr)
            failures += 1
            continue
        print(f"OK   {source.name} -> {destination.name} | {identify(identify_bin, destination)}")

    if failures:
        print(f"Completed with {failures} failure(s). Originals were not modified.", file=sys.stderr)
        return 1
    print(f"Completed {len(inputs)} file(s). Originals were not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
