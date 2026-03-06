# img2pdf

> Convert hundreds of images into a single, ordered PDF — in one command.

A fast, lightweight CLI tool that takes JPG, PNG, WEBP, BMP, and TIFF images and combines them into a single PDF file with smart sorting, custom page sizes, and optional compression.

## Why img2pdf?

Whether you're archiving scanned documents, compiling photo albums, or preparing image-based reports — this tool handles it all from the terminal. Point it at a folder of 200+ images and get a clean, ordered PDF in seconds.

## Quick Start

### Download Binary (No Python Required)

Grab the latest binary for your OS from the [Releases](https://github.com/0xs3c/img2pdf/releases/latest) page:

| Platform | Download |
|----------|----------|
| Linux (x86_64) | `img2pdf-linux-amd64` |
| macOS (Apple Silicon) | `img2pdf-macos-arm64` |
| macOS (Intel) | `img2pdf-macos-amd64` |
| Windows | `img2pdf-windows-amd64.exe` |
```bash
# Make it executable (macOS/Linux)
chmod +x img2pdf-*

# Run it
./img2pdf-macos-arm64 ./photos/ -o album.pdf
```

### Install from Source
```bash
git clone https://github.com/0xs3c/img2pdf.git
cd img2pdf
pip install -e .
```

## Usage
```bash
# Convert an entire folder of images
img2pdf ./photos/ -o album.pdf

# Convert specific files
img2pdf scan1.jpg scan2.jpg scan3.png -o document.pdf

# Sort by date, on A4 pages
img2pdf ./scans/ --sort date --page-size a4 -o report.pdf

# Compress images to reduce file size
img2pdf ./photos/ --quality 60 -o compressed.pdf

# Reverse sort order
img2pdf ./photos/ --sort name --reverse -o album.pdf

# Verbose mode — see every file being processed
img2pdf ./photos/ -o album.pdf --verbose
```

## Options
```
Usage: img2pdf [OPTIONS] SOURCES...

Arguments:
  SOURCES   Image files or directories to convert (required)

Options:
  -o, --output PATH                Output PDF file path       [default: output.pdf]
  -s, --sort [name|date]           Sort by filename or date   [default: name]
  -r, --reverse                    Reverse the sort order
  -p, --page-size [fit|a4|letter]  Page size                  [default: fit]
  -q, --quality INTEGER            Image quality 1-100        [default: 95]
  -v, --verbose                    Show detailed output
  -h, --help                       Show this message and exit
  --version                        Show version
```

## Features

**Smart Sorting** — Natural filename sorting so `img2.jpg` comes before `img10.jpg`. Sort by modification date as an alternative.

**Multiple Formats** — Supports JPG, JPEG, PNG, WEBP, BMP, TIFF out of the box. Transparent PNGs are composited onto a white background automatically.

**Flexible Input** — Pass individual files, entire directories, or a mix of both.

**Page Size Control** — Use `fit` to match each page to its image dimensions, or standardize to `a4` / `letter` with automatic scaling.

**Compression** — Reduce PDF file size by lowering the `--quality` flag. Great for archiving large photo sets.

**Progress Bar** — Visual feedback when processing large batches of images.

## Examples
```bash
# 200 vacation photos → single PDF album
img2pdf ./vacation/ -o vacation-album.pdf

# Scanned documents on A4 pages
img2pdf ./scans/ --page-size a4 -o document.pdf

# Mix files and folders
img2pdf cover.jpg ./chapters/ back.jpg -o book.pdf

# Compressed output for email
img2pdf ./photos/ --quality 50 -o small.pdf
```

## Requirements

- Python 3.8+ (if installing from source)
- No Python needed if using the pre-built binary

## License

[MIT](LICENSE)
