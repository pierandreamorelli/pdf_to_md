from __future__ import annotations

import os


DEFAULT_PROMPT = """Convert this document page to Markdown.

Requirements:
- Return only Markdown, without commentary.
- Preserve headings, paragraphs, lists, formulas, tables and reading order.
- Use Markdown tables for tabular content whenever possible.
- If there are charts, diagrams, figures or photos, add a concise Markdown image note like: ![description](figure-on-page).
- Do not invent text that is not visible in the image.
"""


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "glm-ocr:latest")
OCR_DPI = env_int("OCR_DPI", 200)
PREVIEW_DPI = env_int("PREVIEW_DPI", 120)
OCR_TIMEOUT_SECONDS = env_int("OCR_TIMEOUT_SECONDS", 180)
