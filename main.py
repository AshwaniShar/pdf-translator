# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


    # Use a breakpoint in the code line below to debug your script.
 # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import os
import tempfile

import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator
from docx import Document
from fpdf import FPDF


def extract_text_from_pdf(pdf_path: str) -> str:

    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()  # returns None if page has no text (e.g. scanned image)
            if page_text:
                full_text.append(page_text)
    return "\n\n".join(full_text)


def translate_text(text: str, target_lang: str) -> str:
    if not text.strip():
        return ""

    max_chunk_size = 4500  # stay safely under the ~5000 char limit
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    translator = GoogleTranslator(source="auto", target=target_lang)
    translated_chunks = [translator.translate(chunk) for chunk in chunks]

    return "\n".join(translated_chunks)

def save_as_word(text: str, output_path: str) -> None:
    doc = Document()
    for paragraph in text.split("\n"):
        if paragraph.strip():
            doc.add_paragraph(paragraph)
    doc.save(output_path)


def save_as_pdf(text: str, output_path: str, font_path: str) -> None:
    """Create a Unicode-capable PDF from translated text."""
    if not os.path.isfile(font_path):
        raise FileNotFoundError(
            "DejaVuSans.ttf is required for PDF exports. Place it beside main.py."
        )

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", font_path)
    pdf.set_font("DejaVu", size=12)

    for paragraph in text.split("\n"):
        pdf.multi_cell(0, 8, paragraph)
        pdf.ln(1)

    pdf.output(output_path)


LANGUAGES = {
    "Hindi": "hi", "French": "fr", "Spanish": "es", "German": "de",
    "Japanese": "ja", "Chinese (Simplified)": "zh-CN", "Arabic": "ar",
    "Russian": "ru", "Portuguese": "pt", "Italian": "it",
    "Bengali": "bn", "Tamil": "ta", "Korean": "ko",
}

FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

st.set_page_config(page_title="PDF Translator", page_icon="📄")
st.title("📄 PDF Translator")
st.write("Upload a PDF, choose a language, and download the translated file as PDF or Word.")
st.caption("Created by Ashwani Sharma")

st.markdown(
    "<" "style>"
    '[data-testid="stDeployButton"], .stDeployButton {display: none !important;}'
    "<" "/style>",
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
target_lang_name = st.selectbox("Translate to:", list(LANGUAGES.keys()))
output_format = st.radio("Output format:", ["Word (.docx)", "PDF (.pdf)"])

if uploaded_file is not None and st.button("Translate"):
    # Save the uploaded PDF to a temp file so pdfplumber can open it by path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_pdf_path = tmp.name

    with st.spinner("Reading text from PDF..."):
        original_text = extract_text_from_pdf(tmp_pdf_path)

    if not original_text.strip():
        st.error(
            "Couldn't find any text in this PDF. It might be a scanned image — that needs OCR, which this basic version doesn't include yet.")
    else:
        with st.spinner(f"Translating to {target_lang_name}..."):
            translated_text = translate_text(original_text, LANGUAGES[target_lang_name])

        with st.spinner("Building your output file..."):
            if output_format == "Word (.docx)":
                out_path = "translated_output.docx"
                save_as_word(translated_text, out_path)
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                out_path = "translated_output.pdf"
                save_as_pdf(translated_text, out_path, FONT_PATH)
                mime = "application/pdf"

        st.success("Done!")
        with open(out_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {out_path}",
                data=f,
                file_name=out_path,
                mime=mime,
            )

    os.remove(tmp_pdf_path)

