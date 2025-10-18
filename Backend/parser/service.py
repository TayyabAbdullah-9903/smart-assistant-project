import os
from .utils import extract_text_from_pdf, extract_text_from_docx
from .models import ManualText

def parse_manual_file(manual):
    path = manual.file.path
    ext = os.path.splitext(path)[1].lower()
    pages = []
    if ext == ".pdf":
        pages = extract_text_from_pdf(path)
    elif ext in {".docx", ".doc"}:
        pages = extract_text_from_docx(path)
    for p in pages:
        ManualText.objects.create(manual=manual, page_index=p["page"], text=p["text"])
    manual.processed = True
    manual.save()
