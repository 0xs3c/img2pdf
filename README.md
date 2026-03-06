# img2pdf-cli

A fast CLI tool to convert multiple images (JPG, PNG, WEBP, BMP, TIFF) into a single, ordered PDF file.

## Features

- 🖼️ Supports JPG, PNG, WEBP, BMP, and TIFF formats
- 📁 Convert an entire folder of images in one command
- 🔢 Smart sorting — by filename (natural order) or by date
- 📐 Custom page sizes — A4, Letter, or fit-to-image
- 🗜️ Optional image compression to reduce PDF size
- 📊 Progress bar for large batches

## Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/img2pdf-cli.git
cd img2pdf-cli

# Install in editable mode
pip install -e .
```

## Usage

### Basic — convert a folder of images
```bash
img2pdf ./photos/ -o album.pdf
```

### Convert specific files
```bash
img2pdf image1.jpg image2.png image3.jpg -o output.pdf
```

### Sort by date instead of filename
```bash
img2pdf ./photos/ --sort date -o album.pdf
```

### Use A4 page size with compression
```bash
img2pdf ./photos/ --page-size a4 --quality 80 -o album.pdf
```

### Reverse order
```bash
img2pdf ./photos/ --sort name --reverse -o album.pdf
```

## Options

| Option | Short | Description | Default |
|---|---|---|---|
| `--output` | `-o` | Output PDF path | `output.pdf` |
| `--sort` | `-s` | Sort by: `name` or `date` | `name` |
| `--reverse` | `-r` | Reverse sort order | `False` |
| `--page-size` | `-p` | Page size: `fit`, `a4`, `letter` | `fit` |
| `--quality` | `-q` | JPEG quality 1-100 (lower = smaller file) | `95` |
| `--verbose` | `-v` | Show detailed output | `False` |

## Examples

```bash
# Convert 200 vacation photos sorted by filename
img2pdf ./vacation/ -o vacation-album.pdf

# Convert scanned documents on A4 pages
img2pdf ./scans/ --page-size a4 -o document.pdf

# Quick compressed PDF
img2pdf ./photos/ --quality 60 -o compressed.pdf
```

## License

MIT
