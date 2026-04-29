from __future__ import annotations

import streamlit as st

from config import PREVIEW_DPI
from pdf_processing import PageImage, render_pdf_pages


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #f6f0e7;
            --paper: rgba(255, 252, 246, 0.78);
            --paper-strong: rgba(255, 255, 255, 0.92);
            --ink: #17130f;
            --muted: #746c61;
            --line: rgba(42, 32, 22, 0.12);
            --accent: #9b6230;
            --accent-soft: rgba(155, 98, 48, 0.12);
            --shadow: 0 22px 70px rgba(53, 39, 24, 0.12);
        }

        [data-testid="stHeader"] { display: none; }
        #MainMenu, footer { visibility: hidden; }

        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 16% 6%, rgba(155, 98, 48, 0.18), transparent 30%),
                radial-gradient(circle at 84% 18%, rgba(35, 72, 67, 0.12), transparent 28%),
                linear-gradient(135deg, #fbf6ec 0%, var(--app-bg) 52%, #eee4d8 100%);
        }

        .block-container {
            max-width: 1480px;
            padding: 1.35rem 2.3rem 2.4rem;
        }

        h1, h2, h3, p { font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif; }

        .hero {
            border: 1px solid var(--line);
            border-radius: 28px;
            padding: clamp(1.05rem, 2.2vw, 1.55rem);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.88), rgba(255, 249, 239, 0.62));
            box-shadow: var(--shadow);
            margin-bottom: 0.9rem;
            overflow: hidden;
            position: relative;
        }

        .hero:after {
            content: "";
            position: absolute;
            inset: auto -6% -56% auto;
            width: 24rem;
            height: 24rem;
            border-radius: 999px;
            background: rgba(155, 98, 48, 0.08);
            pointer-events: none;
        }

        .hero-row {
            align-items: flex-end;
            display: flex;
            gap: 2rem;
            justify-content: space-between;
            position: relative;
            z-index: 1;
        }

        .eyebrow, .section-kicker, .mini-label {
            color: var(--accent);
            font-size: 0.74rem;
            font-weight: 760;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .hero h1 {
            color: var(--ink);
            font-size: clamp(2rem, 3.8vw, 4.15rem);
            letter-spacing: -0.065em;
            line-height: 0.96;
            margin: 0.48rem 0 0.55rem;
            max-width: 820px;
        }

        .hero p {
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.52;
            margin: 0;
            max-width: 660px;
        }

        .status-pill, .soft-pill {
            align-items: center;
            background: var(--accent-soft);
            border: 1px solid rgba(155, 98, 48, 0.16);
            border-radius: 999px;
            color: #68411f;
            display: inline-flex;
            font-size: 0.82rem;
            font-weight: 650;
            padding: 0.58rem 0.82rem;
            white-space: nowrap;
        }

        div[data-testid="stFileUploader"] section {
            background: rgba(255, 255, 255, 0.68);
            border: 1px dashed rgba(42, 32, 22, 0.22);
            border-radius: 26px;
            padding: 0.6rem;
        }

        div[data-testid="stFileUploader"] label,
        div[data-testid="stFileUploader"] small {
            color: var(--muted) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 30px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .card-heading {
            align-items: flex-start;
            display: flex;
            gap: 1rem;
            justify-content: space-between;
            margin-bottom: 0.95rem;
        }

        .card-heading h2 {
            color: var(--ink);
            font-size: 1.35rem;
            letter-spacing: -0.035em;
            margin: 0.18rem 0 0;
        }

        .empty-state {
            align-items: center;
            background: rgba(255, 255, 255, 0.54);
            border: 1px solid var(--line);
            border-radius: 24px;
            color: var(--muted);
            display: flex;
            min-height: 440px;
            justify-content: center;
            padding: 2rem;
            text-align: center;
        }

        .prompt-note {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.55;
            margin: -0.15rem 0 0.65rem;
        }

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stPopover"] button {
            border-radius: 999px !important;
            font-weight: 720 !important;
            min-height: 2.85rem;
        }

        .stButton > button[kind="primary"] {
            background: #1b1611 !important;
            border: 1px solid #1b1611 !important;
            color: #fff !important;
            box-shadow: 0 12px 30px rgba(27, 22, 17, 0.18);
        }

        .stDownloadButton > button {
            background: var(--paper-strong) !important;
            border: 1px solid var(--line) !important;
            color: var(--ink) !important;
        }

        textarea,
        div[data-testid="stTextArea"] textarea {
            border-radius: 20px !important;
            border-color: var(--line) !important;
            font-family: "SFMono-Regular", Consolas, monospace !important;
            line-height: 1.5 !important;
        }

        div[data-testid="stTabs"] button {
            color: var(--muted);
            font-weight: 650;
        }

        div[data-testid="stAlert"],
        div[data-testid="stExpander"] {
            border-radius: 20px;
        }

        .page-caption {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin: 0.2rem 0 0.55rem;
            text-transform: uppercase;
        }

        div[data-testid="stImage"] img {
            background: #fff;
            border: 1px solid rgba(42, 32, 22, 0.12) !important;
            border-radius: 18px !important;
            box-shadow: 0 14px 34px rgba(53, 39, 24, 0.10);
        }

        @media (max-width: 900px) {
            .block-container { padding: 1.2rem 1rem 2rem; }
            .hero-row { align-items: flex-start; flex-direction: column; }
            .status-pill { white-space: normal; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="hero-row">
                <div>
                    <div class="eyebrow">GLM-OCR locale</div>
                    <h1>Da PDF complessi a Markdown pulito.</h1>
                    <p>Carica un documento, confronta l'originale con l'OCR e scarica un Markdown leggibile anche quando ci sono tabelle, figure e layout articolati.</p>
                </div>
                <div class="status-pill">Ollama /api/generate</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def card_header(title: str, kicker: str, meta: str | None = None) -> None:
    meta_html = f'<span class="soft-pill">{meta}</span>' if meta else ""
    st.markdown(
        f"""
        <div class="card-heading">
            <div>
                <div class="section-kicker">{kicker}</div>
                <h2>{title}</h2>
            </div>
            {meta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message: str) -> None:
    st.markdown(f'<div class="empty-state">{message}</div>', unsafe_allow_html=True)


def render_empty_comparison() -> None:
    left, right = st.columns([1, 1], gap="large")
    with left:
        with st.container(border=True):
            card_header("Anteprima PDF", "Originale")
            empty_state("Il documento caricato apparira' qui.")
    with right:
        with st.container(border=True):
            card_header("Risultato OCR", "Markdown")
            empty_state("Il Markdown generato apparira' qui dopo la conversione.")


def format_file_size(size_bytes: int) -> str:
    size = float(size_bytes)
    for unit in ("B", "KB", "MB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


@st.cache_data(show_spinner=False)
def get_preview_pages(pdf_bytes: bytes, dpi: int) -> tuple[PageImage, ...]:
    return tuple(render_pdf_pages(pdf_bytes, dpi=dpi))


def show_pdf_preview(pdf_bytes: bytes) -> None:
    with st.spinner("Genero anteprima PDF..."):
        preview_pages = get_preview_pages(pdf_bytes, dpi=PREVIEW_DPI)

    with st.container(height=770, border=False, gap="medium"):
        for page in preview_pages:
            st.markdown(
                f'<div class="page-caption">Pagina {page.page_number}</div>',
                unsafe_allow_html=True,
            )
            st.image(page.png_bytes, width="stretch", output_format="PNG")
