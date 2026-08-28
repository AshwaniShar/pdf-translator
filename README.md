# PDF Translator

A Streamlit application that extracts text from PDF files, translates it into a selected language, and exports the result as a Word document or a Unicode PDF.

## Features

- Extract text from text-based PDF files
- Translate text with Google Translate through `deep-translator`
- Translate into Hindi, French, Spanish, German, Japanese, Simplified Chinese, Arabic, Russian, Portuguese, Italian, Bengali, Tamil, or Korean
- Download translated content as `.docx` or `.pdf`
- Preserve multilingual PDF output with the bundled DejaVu Sans font

## Requirements

- Python 3.14 or newer
- Internet access for translation requests

## Setup

### Using uv

```bash
uv sync
uv run streamlit run main.py
```

### Using pip

```bash
python -m venv .venv
```

Activate the virtual environment, then install the dependencies:

```bash
python -m pip install -e .
streamlit run main.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Usage

1. Open the Streamlit URL shown in the terminal.
2. Upload a text-based PDF.
3. Choose the target language and output format.
4. Select **Translate**.
5. Download the generated Word or PDF file.

## Limitations

- Scanned or image-only PDFs are not supported because OCR is not included.
- Translation is sent through the Google Translate service used by `deep-translator`.
- Very large documents are split into smaller chunks before translation.

## Project Structure

```text
main.py          Streamlit interface and PDF translation logic
pyproject.toml   Project metadata and dependencies
uv.lock          Locked uv dependency versions
DejaVuSans.ttf   Font used for multilingual PDF exports
```

## License

No license has been specified for this project yet.