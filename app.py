from __future__ import annotations

import hashlib

import requests
import streamlit as st

from config import DEFAULT_PROMPT, OCR_DPI, OCR_TIMEOUT_SECONDS, OLLAMA_HOST, OLLAMA_MODEL
from ocr import run_ocr
from pdf_processing import count_pdf_pages
from ui import (
    card_header,
    empty_state,
    format_file_size,
    inject_styles,
    render_empty_comparison,
    render_hero,
    show_pdf_preview,
)


def reset_prompt() -> None:
    st.session_state.ocr_prompt = DEFAULT_PROMPT


def init_page() -> None:
    st.set_page_config(page_title="PDF to Markdown OCR", layout="wide", initial_sidebar_state="collapsed")
    inject_styles()

    if "ocr_prompt" not in st.session_state:
        st.session_state.ocr_prompt = DEFAULT_PROMPT
    if "markdown_result" not in st.session_state:
        st.session_state.markdown_result = ""


def render_upload_and_prompt() -> tuple[bytes, str] | None:
    upload_column, prompt_column = st.columns([0.74, 0.26], gap="large")
    with upload_column:
        uploaded_pdf = st.file_uploader(
            "Carica o trascina un PDF",
            type=["pdf"],
            help="Il file resta locale e viene inviato solo al tuo Ollama in esecuzione sul Mac.",
        )

    with prompt_column:
        st.markdown('<div class="mini-label">Prompt OCR</div>', unsafe_allow_html=True)
        with st.popover("Modifica prompt", use_container_width=True):
            st.markdown(
                '<p class="prompt-note">Personalizza le istruzioni date a GLM-OCR per tabelle, formule, figure e stile Markdown.</p>',
                unsafe_allow_html=True,
            )
            st.text_area("Prompt", key="ocr_prompt", height=300, label_visibility="collapsed")
            st.button("Ripristina prompt", use_container_width=True, on_click=reset_prompt)

    return (uploaded_pdf.getvalue(), uploaded_pdf.name) if uploaded_pdf else None


def clear_stale_result(pdf_bytes: bytes) -> None:
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    if st.session_state.get("pdf_hash") != pdf_hash:
        st.session_state.pdf_hash = pdf_hash
        st.session_state.markdown_result = ""


def render_pdf_panel(pdf_bytes: bytes, page_count: int) -> None:
    file_meta = f"{page_count} pagine / {format_file_size(len(pdf_bytes))}"
    with st.container(border=True):
        card_header("Anteprima PDF", "Originale", file_meta)
        show_pdf_preview(pdf_bytes)


def render_markdown_panel(pdf_bytes: bytes, pdf_name: str) -> None:
    with st.container(border=True):
        card_header("Risultato OCR", "Markdown")
        button_label = "Rigenera Markdown" if st.session_state.markdown_result else "Converti in Markdown"

        if st.button(button_label, type="primary", use_container_width=True):
            progress = st.progress(0, text="Preparazione OCR...")

            def update_progress(value: float, text: str) -> None:
                progress.progress(value, text=text)

            try:
                st.session_state.markdown_result = run_ocr(
                    pdf_bytes=pdf_bytes,
                    dpi=OCR_DPI,
                    prompt=st.session_state.ocr_prompt,
                    host=OLLAMA_HOST,
                    model=OLLAMA_MODEL,
                    timeout_seconds=OCR_TIMEOUT_SECONDS,
                    progress_callback=update_progress,
                )
            except requests.ConnectionError:
                st.error("Impossibile contattare Ollama. Verifica che `ollama serve` sia attivo.")
            except requests.HTTPError as exc:
                status = exc.response.status_code if exc.response is not None else "sconosciuto"
                body = exc.response.text if exc.response is not None else str(exc)
                st.error(f"Errore Ollama HTTP {status}: {body}")
            except Exception as exc:
                st.error(f"OCR non riuscito: {exc}")

        markdown_result = st.session_state.markdown_result
        if not markdown_result:
            empty_state("Pronto per l'OCR. Premi Converti in Markdown per iniziare.")
            return

        st.download_button(
            "Scarica Markdown",
            data=markdown_result.encode("utf-8"),
            file_name=f"{pdf_name.rsplit('.', 1)[0]}.md",
            mime="text/markdown",
            use_container_width=True,
        )
        preview_tab, source_tab = st.tabs(["Preview", "Sorgente"])
        with preview_tab:
            st.markdown(markdown_result)
        with source_tab:
            st.code(markdown_result, language="markdown")


def render_comparison(pdf_bytes: bytes, pdf_name: str) -> None:
    clear_stale_result(pdf_bytes)

    try:
        page_count = count_pdf_pages(pdf_bytes)
    except Exception as exc:
        st.error(f"PDF non leggibile: {exc}")
        return

    left, right = st.columns([1, 1], gap="large")
    with left:
        render_pdf_panel(pdf_bytes, page_count)
    with right:
        render_markdown_panel(pdf_bytes, pdf_name)


def main() -> None:
    init_page()
    render_hero()

    uploaded_pdf = render_upload_and_prompt()
    if uploaded_pdf is None:
        render_empty_comparison()
        return

    pdf_bytes, pdf_name = uploaded_pdf
    render_comparison(pdf_bytes, pdf_name)


if __name__ == "__main__":
    main()
