"""qrkie CLI implementation.

QR code generator
"""

from enum import Enum

import sys
import qrcode
from qrcode.image.styledpil import StyledPilImage


import zipfile
import typer
from pathlib import Path
from loguru import logger
from datetime import datetime
from .self_subcommand import cli as self_cli
from .settings import Settings

from .record import URLRecord
from .style import Style


cli = typer.Typer()

cli.add_typer(
    self_cli,
    name="self",
    help="Manage the qrkie command.",
)


@cli.callback(invoke_without_command=True, no_args_is_help=True)
def global_callback(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False,
        "--debug",
        "-D",
        help="Enable debugging output.",
    ),
) -> None:
    """QR code generator"""
    ctx.obj = Settings()
    debug = debug or ctx.obj.debug
    (logger.enable if debug else logger.disable)("qrkie")
    logger.add("qrkie.log")
    logger.info(f"{debug=}")


@cli.command(name="batch", help="Generate a QR code from the provided data.")
def batch_qr_codes(
    ctx: typer.Context,
    sep: str = typer.Option(
        "|",
        "--sep",
        "-s",
        help="Separator between name and URL in the input file.",
    ),
    input_file: Path = typer.Option(
        ...,
        "--input-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    output_formats: list[str] = typer.Option("eps", "--format", "-f"),
    prefix: str = typer.Option("", "--prefix", "-P"),
    pixels: int = typer.Option(
        1000,
        "--pixels",
        "-p",
        help="Number of pixels per QR code module.",
    ),
    zip: bool = typer.Option(False, "--zip", "-z"),
    normalize: bool = typer.Option(False, "--normalize-size", "-n"),
    version: str | None = typer.Option(None, "--version", "-V"),
    styles: list[Style] | None = typer.Option([Style.square], "--style", "-S"),
    all_styles: bool = typer.Option(False, "--all-styles", "-A"),
) -> None:
    """Generate a QR code for the given url and write to OUTPUT_FILE."""

    if all_styles:
        styles = list(Style)

    prefix = f"{prefix}-" if prefix else ""

    if zip:
        folder_name = f"{prefix}QR-Codes-{datetime.now():%Y%m%d-%H%M%S}"
        archive = zipfile.ZipFile(f"{folder_name}.zip", mode="w")
        archive.mkdir(folder_name)

    for record in sorted(
        URLRecord.from_file(input_file, sep=sep),
        reverse=True,
    ):
        qr_code = record.qrcode(version=version)

        if normalize and version == None:
            qr_code.make(fit=True)
            version = qr_code.version

        for output_format in output_formats:
            for style in styles:
                filename = record.filename(
                    prefix=f"{prefix}QR-Code",
                    extension=output_format,
                    version=qr_code.version,
                    style=style.name,
                )

                img = qr_code.make_image(module_drawer=style.drawer)

                match output_format.lower():
                    case "png":
                        img = img.resize((pixels, pixels))

                img.save(filename)

                try:
                    archive.write(filename, f"{folder_name}/{filename}")
                    Path(filename).unlink()
                except UnboundLocalError:
                    logger.info(f"Saved QR code to {filename}")

    try:
        logger.info(f"Created archive: {folder_name}.zip")
        logger.info(f"Folder name: {folder_name}")
        logger.info(f"Contents of the archive:")
        for name in archive.namelist():
            logger.info(f"File: {name}")
    except Exception as error:
        pass


@cli.command(name="code")
def generate_qr_code(
    ctx: typer.Context,
    data: str = typer.Argument(..., help="Data to encode in the QR code."),
    basename: str = typer.Option("qrcode", "--output-filename", "-o"),
    output_formats: list[str] = typer.Option(
        ["png"],
        "--format",
        "-f",
        help="Output file format(s). Can be specified multiple times.",
    ),
    version: str | None = typer.Option(None, "--version", "-V"),
    styles: list[Style] | None = typer.Option([Style.square], "--style", "-S"),
    all_styles: bool = typer.Option(False, "--all-styles", "-A"),
    pixels: int = typer.Option(1000, "--pixels", "-p", help="PNG pixel dimensions."),
) -> None:
    """Generate a QR code for the given data and write to OUTPUT_FILE."""

    record = URLRecord(url=data, description=basename)

    if all_styles:
        styles = list(Style)

    for output_format in output_formats:
        for style in styles:
            qr_code = record.qrcode(version=version)
            filename = record.filename(
                extension=output_format,
                version=qr_code.version,
                style=style.name,
            )
            img = qr_code.make_image(module_drawer=style.drawer)

            img.save(filename)


if __name__ == "__main__":
    sys.exit(cli())
