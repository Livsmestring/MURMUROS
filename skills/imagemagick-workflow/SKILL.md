---
name: imagemagick-workflow
description: Reliable image conversion and batch manipulation with ImageMagick. Use for resizing, format conversion, compression, cropping, thumbnails, metadata inspection, compositing, and other deterministic image-processing tasks involving local files.
---

# ImageMagick Workflow

Use ImageMagick as the default battle-tested CLI for deterministic image conversion and manipulation. Prefer it over writing custom image-processing code when the task is a standard transformation.

## Operating procedure

1. Identify the input files, desired output format, dimensions, quality, naming convention, and whether the user wants to preserve metadata or transparency.
2. Check that ImageMagick is available with `magick -version` or, on older installations, `convert -version`.
3. Inspect inputs before changing them. Use `identify -verbose INPUT` for dimensions, color space, alpha, format, and metadata. Never overwrite the original unless the user explicitly requests it.
4. Choose the narrowest command that satisfies the request. Keep output in a separate directory and use explicit output filenames or a controlled glob.
5. Run the transformation. For batch work, process only the intended extensions and avoid recursive traversal unless requested.
6. Verify every output with `identify`, checking file existence, format, dimensions, and expected transparency. Report failures rather than silently skipping them.
7. Deliver the output files and state the exact transformation, quality settings, and any limitations.

## Safety and quality rules

- Treat filenames and downloaded content as untrusted data. Quote paths and do not execute files merely because they are images.
- Validate input paths and output destinations before processing. Do not delete, move, or overwrite source files without explicit authorization.
- Use `--` where supported and quote shell paths containing spaces or shell metacharacters.
- Use bounded dimensions and avoid constructing commands from unsanitized user input.
- Preserve aspect ratio by default. Use `^`, `!`, or cropping only when the user explicitly wants fill or exact dimensions.
- Preserve transparency when the target format supports it. Do not convert transparent images to JPEG without warning that transparency will be flattened.
- For web delivery, use a deliberate quality setting and verify the resulting file size; do not claim that compression is lossless unless it is.
- Prefer `magick` syntax. Fall back to `convert` only when `magick` is unavailable.

## Common recipes

### Convert a single image

```bash
magick -- input.tif output.png
```

Use the equivalent `convert -- input.tif output.png` on older installations.

### Resize while preserving aspect ratio

```bash
magick -- input.jpg -resize '1600x1600>' output.jpg
```

The `>` prevents upscaling smaller images. Use `1600x1600^` followed by `-gravity center -extent 1600x1600` when the user wants a filled square crop.

### Create a thumbnail

```bash
magick -- input.jpg -auto-orient -thumbnail '320x320>' -strip output-thumb.jpg
```

Use `-auto-orient` for camera images. Use `-strip` only when removing metadata is acceptable.

### Convert SVG or another source to PNG

```bash
magick -- input.svg -background none output.png
identify output.png
```

If the SVG contains external references or untrusted content, inspect it first and avoid enabling arbitrary delegates.

### Compress JPEG for web delivery

```bash
magick -- input.png -auto-orient -strip -sampling-factor 4:2:0 -quality 82 output.jpg
identify output.jpg
```

State that this is lossy compression and that alpha transparency is flattened against the default background unless a background is specified.

### Batch-convert selected files

```bash
mkdir -p output
for input in input/*.png; do
  [ -f "$input" ] || continue
  name=${input##*/}
  name=${name%.png}
  magick -- "$input" -resize '2000x2000>' "output/${name}.jpg"
done
```

Use a temporary output directory or a distinct extension to avoid collisions. For mixed extensions, enumerate the allowed patterns explicitly.

### Add a solid background before JPEG conversion

```bash
magick -- input.png -background white -alpha remove -alpha off -quality 85 output.jpg
```

Choose the background color deliberately and mention that transparency was removed.

## Verification checklist

For each output, verify:

```bash
identify -format '%f | %m | %wx%h | %[channels] | %b\n' -- output-file
```

Check that the file exists, the format is the requested format, dimensions match the request, alpha channels are present or absent as intended, and the byte size is plausible. For visually important edits, use image viewing rather than relying only on metadata.

## Response pattern

Give the user a concise completion summary containing:

- the source and output paths;
- the operation and important parameters;
- verification results such as format, dimensions, and file size;
- any lossy, transparency, metadata, color-profile, or upscaling caveats; and
- a link to the [ImageMagick project](https://github.com/ImageMagick/ImageMagick) when crediting the tool.

If the request is ambiguous, ask only for the missing choice that changes the output, such as exact dimensions, target format, background color, or whether metadata should be preserved.

## Examples

**Input:** “Turn these product PNGs into web-ready JPEGs, max 1600 px wide, keep the originals.”

**Approach:** Inspect all inputs, create a separate output directory, use `-resize '1600x1600>' -strip -quality 82`, verify each JPEG, and report that transparency and metadata were removed or flattened as applicable.

**Input:** “Make square thumbnails from these portraits without stretching them.”

**Approach:** Use `-auto-orient`, resize to cover the square, crop from the center or the user-selected gravity, and verify exact square dimensions.

**Input:** “Convert this logo SVG to a transparent PNG.”

**Approach:** Use `-background none`, preserve alpha, verify the PNG channels, and avoid claiming visual correctness without inspecting the rendered output.

## Reusable batch utility

For repeatable directory conversions, use the bundled `scripts/convert_images.py` rather than composing an ad hoc shell loop. It uses subprocess argument arrays, never overwrites inputs, rejects an output directory equal to the input directory, supports bounded dimensions, optional metadata stripping, optional quality settings, and verifies every successful output.

Example:

```bash
python3 /home/ubuntu/skills/imagemagick-workflow/scripts/convert_images.py \
  ./input ./output \
  --format jpg \
  --max-width 1600 \
  --max-height 1600 \
  --quality 82 \
  --strip-metadata
```

The utility accepts supported local image files in the input directory and returns a non-zero status if any file fails or an output already exists. Treat an existing output as a review condition rather than silently replacing it.

## Package contents

- `SKILL.md`: trigger metadata, decision rules, recipes, safety guidance, verification, and response format.
- `scripts/convert_images.py`: deterministic, non-shell batch conversion utility for repeatable jobs.

Do not add README files, credentials, user data, or generated output files to the skill package.

## Automated test suite

Run the bundled integration tests after changing the utility or its workflow:

```bash
python3 /home/ubuntu/skills/imagemagick-workflow/scripts/test_convert_images.py
```

The suite uses only Python’s standard library and temporary directories. It covers SVG-to-PNG conversion, bounded resizing and no-upscale behavior, JPEG quality/background/metadata options, preservation of originals, rejection of identical input/output directories, refusal to overwrite existing outputs, ignoring unsupported files, empty-input rejection, invalid quality validation, corrupt-input reporting, and successful verification through `identify`.

The test environment must provide ImageMagick’s `identify` plus either `magick` or `convert`. A missing dependency causes the suite to skip rather than produce a misleading pass.
