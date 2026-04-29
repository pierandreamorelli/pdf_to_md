#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-glm-ocr:latest}"
export OLLAMA_HOST OLLAMA_MODEL

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  printf 'Errore: %s non trovato. Installa Python 3.10+ e riprova.\n' "$PYTHON_BIN" >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if ! command -v ollama >/dev/null 2>&1; then
  printf 'Errore: Ollama non trovato. Installa Ollama e poi esegui: ollama pull %s\n' "$OLLAMA_MODEL" >&2
  exit 1
fi

if ! curl --silent --fail "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
  printf 'Ollama non risponde su %s. Avvio ollama serve in background...\n' "$OLLAMA_HOST"
  ollama serve >/tmp/pdf_to_md_ollama.log 2>&1 &
  sleep 3
fi

if ! curl --silent --fail "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
  printf 'Errore: Ollama non risponde ancora. Log: /tmp/pdf_to_md_ollama.log\n' >&2
  exit 1
fi

if ! ollama show "$OLLAMA_MODEL" >/dev/null 2>&1; then
  printf 'Modello %s non trovato. Download in corso...\n' "$OLLAMA_MODEL"
  ollama pull "$OLLAMA_MODEL"
fi

streamlit run app.py
