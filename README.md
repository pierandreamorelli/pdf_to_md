# PDF to Markdown OCR

Webapp Python minimale per caricare un PDF, visualizzarlo a sinistra e generare Markdown a destra usando `glm-ocr` tramite Ollama locale.

## Prerequisiti

- Mac con macOS.
- Git, solo se vuoi scaricare il progetto con `git clone`.
- Python 3.10 o superiore.
- Ollama installato.
- Almeno 8 GB di RAM consigliati. Con 6 GB puo' funzionare su PDF piccoli, ma non e' garantito.
- Almeno 5 GB liberi su disco per modello, ambiente Python e file temporanei.
- Connessione internet al primo avvio per scaricare dipendenze e modello OCR.

## Getting Started

Questa app gira in locale sul tuo Mac.

### 1. Installa Homebrew, se non lo hai

Controlla se hai gia' Homebrew:

```bash
brew --version
```

Se il comando da' errore, installalo da qui:

- [https://brew.sh](https://brew.sh)

Oppure incolla questo comando nel Terminale:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Alla fine dell'installazione, se Homebrew ti mostra uno o due comandi da copiare nel Terminale, copiali ed eseguili.

### 2. Installa Python

```bash
brew install python
```

Controlla che funzioni:

```bash
python3 --version
```

Serve Python 3.10 o superiore.

### 3. Installa Ollama

Metodo consigliato: scaricalo dal sito ufficiale.

- [https://ollama.com/download/mac](https://ollama.com/download/mac)

Alternativa con Homebrew:

```bash
brew install --cask ollama
```

Controlla che funzioni:

```bash
ollama --version
```

### 4. Scarica il progetto

Metodo consigliato con Git:

```bash
git clone https://github.com/pierandreamorelli/pdf_to_md.git
cd pdf_to_md
```

Sostituisci `<URL_DELLA_REPO>` con l'URL GitHub del progetto.

Se `git clone` non funziona, installa Git:

```bash
brew install git
```

Alternativa senza Git:

- apri la repo su GitHub
- premi `Code`
- premi `Download ZIP`
- decomprimi lo ZIP
- apri il Terminale nella cartella decompressa

### 5. Avvia l'app

```bash
chmod +x start.sh
./start.sh
```

Lo script fa tutto il resto:

- crea l'ambiente Python `.venv`
- installa le dipendenze
- avvia Ollama se non e' gia' attivo
- scarica `glm-ocr:latest` se manca
- apre Streamlit nel browser

Alla fine dovresti vedere un link tipo:

```text
Local URL: http://localhost:8501
```

Apri quel link nel browser.

## Uso

- Carica un PDF.
- Se serve, premi `Modifica prompt` per personalizzare le istruzioni OCR.
- Premi `Converti in Markdown`.
- Confronta PDF e Markdown.
- Scarica il file `.md`.

## Errori comuni

### `zsh: permission denied: ./start.sh`

Esegui:

```bash
chmod +x start.sh
./start.sh
```

### `Errore: python3 non trovato`

Installa Python:

```bash
brew install python
```

Poi riprova:

```bash
./start.sh
```

### `Errore: Ollama non trovato`

Installa Ollama:

- [https://ollama.com/download/mac](https://ollama.com/download/mac)

Oppure:

```bash
brew install --cask ollama
```

Poi riprova:

```bash
./start.sh
```

### `Errore: Ollama non risponde ancora`

Avvia Ollama manualmente:

```bash
ollama serve
```

Lascia aperto quel Terminale, aprine un altro nella cartella del progetto ed esegui:

```bash
./start.sh
```

### `Impossibile contattare Ollama`

Significa che la webapp non riesce a parlare con Ollama su `http://localhost:11434`.

Prova questi comandi:

```bash
ollama serve
```

Poi, in un altro Terminale:

```bash
curl http://localhost:11434/api/tags
```

Se `curl` risponde con una lista di modelli, riavvia l'app:

```bash
./start.sh
```

### Il primo avvio e' lento

E' normale. Al primo avvio lo script scarica il modello `glm-ocr:latest`, che puo' richiedere diversi minuti.

### Su Streamlit Cloud non funziona

E' previsto: Streamlit Cloud non ha accesso al tuo Ollama locale. Per condividerla senza installazione locale serve un server tuo con Ollama oppure una API cloud al posto di Ollama.

## Requisiti tecnici

- Python 3.10+
- Ollama su macOS
- Modello `glm-ocr:latest`, scaricato automaticamente da `start.sh`

## Avvio manuale

Usa questa procedura solo se non vuoi usare `./start.sh`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull glm-ocr:latest
streamlit run app.py
```

Se Ollama non e' gia' attivo:

```bash
ollama serve
```

## Configurazione opzionale

La UI resta minimale. Le impostazioni tecniche si configurano con variabili d'ambiente prima di avviare `./start.sh`.


| Variabile             | Default                  | Scopo                                      |
| --------------------- | ------------------------ | ------------------------------------------ |
| `OLLAMA_HOST`         | `http://localhost:11434` | Endpoint locale di Ollama                  |
| `OLLAMA_MODEL`        | `glm-ocr:latest`         | Modello OCR da usare                       |
| `OCR_DPI`             | `200`                    | Risoluzione di rendering delle pagine PDF  |
| `PREVIEW_DPI`         | `120`                    | Risoluzione dell'anteprima visuale del PDF |
| `OCR_TIMEOUT_SECONDS` | `180`                    | Timeout massimo per pagina                 |


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

