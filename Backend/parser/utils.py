import fitz  # PyMuPDF
from docx import Document
from typing import List, Dict

def extract_text_from_pdf(path: str) -> List[Dict]:
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text and text.strip():
            pages.append({"page": i+1, "text": text})
    return pages

def extract_text_from_docx(path: str) -> List[Dict]:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    # return as single "page" for simplicity
    return [{"page": 1, "text": "\n".join(paragraphs)}]

def chunk_text(text: str, max_chars: int = 3000):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+max_chars])
        start += max_chars
    return chunks
