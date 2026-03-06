import os
import re
from pathlib import Path
from typing import List

from PIL import Image
from tqdm import tqdm

# Supported image extensions
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}

# Page size dimensions in points (72 points = 1 inch)
PAGE_SIZES = {
    "a4": (595.28, 841.89),
    "letter": (612, 792),
}


def natural_sort_key(path: Path):
    """Sort filenames naturally so img2.jpg comes before img10.jpg."""
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def date_sort_key(path: Path):
    """Sort by file modification time."""
    return os.path.getmtime(path)


def collect_images(sources: List[str]) -> List[Path]:
    """
    Collect image paths from a mix of files and directories.

    Args:
        sources: List of file paths or directory paths.

    Returns:
        List of Path objects pointing to valid image files.
    """
    images = []

    for source in sources:
        path = Path(source)

        if path.is_dir():
            for item in path.iterdir():
                if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                    images.append(item)
        elif path.is_file():
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                images.append(path)
            else:
                raise ValueError(
                    f"Unsupported file format: {path.name} "
                    f"(supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))})"
                )
        else:
            raise FileNotFoundError(f"Path not found: {source}")

    if not images:
        raise ValueError("No valid images found in the provided paths.")

    return images


def sort_images(images: List[Path], sort_by: str = "name", reverse: bool = False) -> List[Path]:
    """
    Sort image paths by name or date.

    Args:
        images: List of image paths.
        sort_by: 'name' for natural filename sort, 'date' for modification time.
        reverse: Reverse the sort order.

    Returns:
        Sorted list of image paths.
    """
    if sort_by == "name":
        key_func = natural_sort_key
    elif sort_by == "date":
        key_func = date_sort_key
    else:
        raise ValueError(f"Unknown sort method: {sort_by}. Use 'name' or 'date'.")

    return sorted(images, key=key_func, reverse=reverse)


def prepare_image(image_path: Path, page_size: str = "fit", quality: int = 95) -> Image.Image:
    """
    Open and prepare an image for PDF inclusion.

    Args:
        image_path: Path to the image file.
        page_size: 'fit' to use image dimensions, 'a4' or 'letter' for standard sizes.
        quality: JPEG compression quality (1-100).

    Returns:
        Prepared PIL Image in RGB mode.
    """
    img = Image.open(image_path)

    # Convert to RGB (required for PDF — handles RGBA, palette, etc.)
    if img.mode in ("RGBA", "LA"):
        # Composite onto white background
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize to fit page if needed
    if page_size != "fit" and page_size in PAGE_SIZES:
        page_w, page_h = PAGE_SIZES[page_size]
        img_w, img_h = img.size
        scale = min(page_w / img_w, page_h / img_h)
        if scale < 1:
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)

    return img


def images_to_pdf(
    sources: List[str],
    output: str = "output.pdf",
    sort_by: str = "name",
    reverse: bool = False,
    page_size: str = "fit",
    quality: int = 95,
    verbose: bool = False,
) -> str:
    """
    Convert multiple images into a single PDF file.

    Args:
        sources: List of image files or directories.
        output: Output PDF file path.
        sort_by: Sort method ('name' or 'date').
        reverse: Reverse sort order.
        page_size: Page size ('fit', 'a4', 'letter').
        quality: JPEG quality for compression (1-100).
        verbose: Print detailed info.

    Returns:
        Path to the created PDF file.
    """
    # Step 1: Collect all images
    images = collect_images(sources)

    # Step 2: Sort them
    images = sort_images(images, sort_by=sort_by, reverse=reverse)

    if verbose:
        print(f"\nFound {len(images)} images:")
        for i, img in enumerate(images, 1):
            print(f"  {i:>4}. {img.name}")
        print()

    # Step 3: Convert and build PDF
    pdf_images = []
    desc = "Converting images"

    for image_path in tqdm(images, desc=desc, disable=not verbose and len(images) < 10):
        try:
            prepared = prepare_image(image_path, page_size=page_size, quality=quality)
            pdf_images.append(prepared)
        except Exception as e:
            print(f"  ⚠ Skipping {image_path.name}: {e}")

    if not pdf_images:
        raise ValueError("No images could be processed successfully.")

    # Step 4: Save as PDF
    first_image = pdf_images[0]
    remaining = pdf_images[1:] if len(pdf_images) > 1 else []

    first_image.save(
        output,
        "PDF",
        save_all=True,
        append_images=remaining,
        quality=quality,
    )

    return output
