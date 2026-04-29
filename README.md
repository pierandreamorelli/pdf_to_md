# PDF to Markdown OCR

Webapp Python minimale per caricare un PDF, visualizzarlo a sinistra e generare Markdown a destra usando `glm-ocr` tramite Ollama locale.

## Requisiti

- Python 3.10+
- Ollama attivo su macOS
- Modello installato: `ollama pull glm-ocr:latest`

## Avvio

Avvio automatico:

```bash
chmod +x start.sh
./start.sh
```

Lo script crea `.venv`, installa le dipendenze, controlla Ollama, scarica `glm-ocr:latest` se manca e avvia Streamlit.

Avvio manuale:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Se Ollama non e' gia' attivo:

```bash
ollama serve
```

## Uso

1. Apri la webapp nel browser.
2. Carica un PDF.
3. Se serve, premi `Modifica prompt` per personalizzare le istruzioni OCR.
4. Premi `Converti in Markdown`.
5. Confronta PDF e Markdown, poi scarica il file `.md`.

## Configurazione opzionale

La UI resta minimale. Le impostazioni tecniche si configurano con variabili d'ambiente prima di avviare `./start.sh`.

| Variabile | Default | Scopo |
| --- | --- | --- |
| `OLLAMA_HOST` | `http://localhost:11434` | Endpoint locale di Ollama |
| `OLLAMA_MODEL` | `glm-ocr:latest` | Modello OCR da usare |
| `OCR_DPI` | `200` | Risoluzione di rendering delle pagine PDF |
| `PREVIEW_DPI` | `120` | Risoluzione dell'anteprima visuale del PDF |
| `OCR_TIMEOUT_SECONDS` | `180` | Timeout massimo per pagina |

## Struttura

- `app.py`: composizione della pagina Streamlit, stato e gestione errori.
- `config.py`: prompt predefinito e variabili d'ambiente.
- `pdf_processing.py`: conteggio e rendering pagine PDF in PNG.
- `ocr.py`: chiamate a Ollama e conversione pagina-per-pagina.
- `ui.py`: CSS, componenti visuali e anteprima PDF.

## Note

- La conversione avviene pagina per pagina: ogni pagina del PDF viene renderizzata come PNG e inviata a Ollama con `/api/generate`.
- Anche l'anteprima viene renderizzata come immagini, cosi' non dipende dal viewer PDF del browser.
- Aumentare la risoluzione migliora spesso l'OCR, ma rende le richieste piu' lente.
- Per documenti lunghi la conversione puo' richiedere tempo, perche' ogni pagina viene processata separatamente.
