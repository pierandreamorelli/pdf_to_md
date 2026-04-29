from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import fitz


@dataclass(frozen=True)
class PageImage:
    page_number: int
    png_bytes: bytes


def count_pdf_pages(pdf_bytes: bytes) -> int:
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        return len(document)


def render_pdf_pages(pdf_bytes: bytes, dpi: int) -> Iterable[PageImage]:
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        for index in range(len(document)):
            page = document.load_page(index)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            yield PageImage(page_number=index + 1, png_bytes=pixmap.tobytes("png"))
