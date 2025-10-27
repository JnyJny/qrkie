""" """

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from functools import cached_property
from qrcode.image.styledpil import StyledPilImage

import qrcode


@dataclass
class URLRecord:
    description: str
    url: str

    @classmethod
    def from_file(cls, path: str | Path, sep: str = "|") -> list[URLRecord]:
        path = Path(path)
        records = []
        for line in path.read_text().splitlines():
            description, url = line.split(sep, maxsplit=1)
            records.append(cls(description=description.strip(), url=url.strip()))

        return records

    def __lt__(self, other: URLRecord) -> bool:
        if not isinstance(other, URLRecord):
            raise NotImplementedError
        return len(self.url) < len(other.url)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, URLRecord):
            raise NotImplementedError
        return self.url == other.url

    def __str__(self) -> str:
        return self.url

    @cached_property
    def basename(self) -> str:
        """Return a filesystem-safe base name for the record."""

        tt = str.maketrans(
            {
                ".": "",
                " ": "-",
                "/": "-",
                "\\": "-",
                ":": "-",
                "*": "",
                "?": "",
                '"': "",
                "<": "",
                ">": "",
                "|": "",
            }
        )

        return self.description.translate(tt).lower()

    def filename(
        self,
        extension: str,
        prefix: str | None = None,
        version: str | None = None,
        style: str | None = None,
        sep: str = "-",
    ) -> str:
        """Return a filename for the record."""

        if extension.startswith("."):
            extension = extension[1:]

        prefix = f"{prefix}{sep}" if prefix else ""
        style = f"{sep}{style}" if style else ""
        version = f"{sep}{version}" if version else ""

        return f"{prefix}{self.basename}{style}{version}.{extension}"

    def qrcode(self, version: str | int | None = None) -> qrcode.QRCode:
        """Return a QRCode object for the record's URL."""
        qr = qrcode.QRCode(
            version=version,
            image_factory=StyledPilImage,
            border=0,
        )
        qr.add_data(self.url)
        qr.make(fit=True)
        return qr
