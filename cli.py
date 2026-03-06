import os
import sys
import time

import click

from img2pdf_cli import __version__
from img2pdf_cli.converter import images_to_pdf


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("sources", nargs=-1, required=True, type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    default="output.pdf",
    show_default=True,
    help="Output PDF file path.",
)
@click.option(
    "-s", "--sort",
    "sort_by",
    type=click.Choice(["name", "date"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sort images by filename or modification date.",
)
@click.option(
    "-r", "--reverse",
    is_flag=True,
    default=False,
    help="Reverse the sort order.",
)
@click.option(
    "-p", "--page-size",
    type=click.Choice(["fit", "a4", "letter"], case_sensitive=False),
    default="fit",
    show_default=True,
    help="Page size: 'fit' matches image dimensions.",
)
@click.option(
    "-q", "--quality",
    type=click.IntRange(1, 100),
    default=95,
    show_default=True,
    help="Image quality (1-100). Lower = smaller file size.",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    default=False,
    help="Show detailed output.",
)
@click.version_option(version=__version__, prog_name="img2pdf")
def main(sources, output, sort_by, reverse, page_size, quality, verbose):
    """Convert images to a single PDF file.

    SOURCES can be image files and/or directories containing images.

    \b
    Supported formats: JPG, PNG, WEBP, BMP, TIFF

    \b
    Examples:
      img2pdf ./photos/ -o album.pdf
      img2pdf img1.jpg img2.jpg -o output.pdf
      img2pdf ./scans/ --page-size a4 --sort date -o doc.pdf
    """
    try:
        start = time.time()

        result = images_to_pdf(
            sources=list(sources),
            output=output,
            sort_by=sort_by,
            reverse=reverse,
            page_size=page_size,
            quality=quality,
            verbose=verbose,
        )

        elapsed = time.time() - start

        # Get file size
        size_bytes = os.path.getsize(result)
        if size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

        click.echo(f"\nPDF created: {result} ({size_str}) in {elapsed:.1f}s")

    except FileNotFoundError as e:
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nUnexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
