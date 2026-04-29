from __future__ import annotations

import base64
from collections.abc import Callable

import requests

from pdf_processing import count_pdf_pages, render_pdf_pages


ProgressCallback = Callable[[float, str], None]


def call_ollama_ocr(
    *,
    image_bytes: bytes,
    prompt: str,
    host: str,
    model: str,
    timeout_seconds: int,
) -> str:
    url = f"{host.rstrip('/')}/api/generate"
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
        "options": {"temperature": 0},
    }

    response = requests.post(url, json=payload, timeout=timeout_seconds)
    response.raise_for_status()
    data = response.json()

    result = data.get("response")
    if not isinstance(result, str):
        raise RuntimeError(f"Risposta Ollama inattesa: {data}")
    return result.strip()


def run_ocr(
    *,
    pdf_bytes: bytes,
    dpi: int,
    prompt: str,
    host: str,
    model: str,
    timeout_seconds: int,
    progress_callback: ProgressCallback | None = None,
) -> str:
    page_count = count_pdf_pages(pdf_bytes)
    if page_count == 0:
        return ""

    if progress_callback:
        progress_callback(0, "Preparazione OCR...")

    markdown_parts: list[str] = []
    for index, page in enumerate(render_pdf_pages(pdf_bytes, dpi=dpi), start=1):
        if progress_callback:
            progress_callback((index - 1) / page_count, f"OCR pagina {page.page_number} di {page_count}...")

        page_markdown = call_ollama_ocr(
            image_bytes=page.png_bytes,
            prompt=prompt,
            host=host,
            model=model,
            timeout_seconds=timeout_seconds,
        )
        markdown_parts.append(f"<!-- page: {page.page_number} -->\n\n{page_markdown}")

    if progress_callback:
        progress_callback(1.0, "OCR completato")

    return "\n\n---\n\n".join(markdown_parts)
