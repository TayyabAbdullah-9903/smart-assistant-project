import os
import re
import fitz  # PyMuPDF
from docx import Document
from .models import ManualText


def clean_text(text):
    """Clean and normalize extracted text."""
    if not text:
        return ""
    # Remove null bytes and excessive whitespace
    text = text.replace("\x00", "").replace("\r", "\n")
    # Normalize multiple spaces but preserve line breaks
    text = re.sub(r' +', ' ', text)
    # Remove excessive blank lines (more than 2)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def extract_text_from_pdf(path):
    """
    Extract text from PDF with improved structure preservation.
    Returns a list of dicts: [{"page": 1, "text": "..."}]
    """
    pages = []
    try:
        with fitz.open(path) as doc:
            for i, page in enumerate(doc):
                # Extract text blocks to preserve layout
                blocks = page.get_text("blocks")
                
                # Sort blocks by vertical then horizontal position
                blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
                
                # Combine blocks into coherent text
                text_parts = []
                for block in blocks:
                    block_text = block[4] if len(block) > 4 else ""
                    if block_text.strip():
                        text_parts.append(block_text.strip())
                
                full_text = "\n\n".join(text_parts)
                full_text = clean_text(full_text)
                
                if full_text:  # Only save non-empty pages
                    pages.append({"page": i + 1, "text": full_text})
                    
    except Exception as e:
        print(f"[PDF Parse Error] {path}: {e}")
    return pages


def extract_text_from_docx(path):
    """
    Extract text from DOCX with structure preservation.
    """
    pages = []
    try:
        doc = Document(path)
        sections = []
        current_section = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                if current_section:  # Blank line = section break
                    sections.append("\n".join(current_section))
                    current_section = []
                continue
            
            # Preserve heading structure
            if para.style.name.startswith('Heading'):
                if current_section:
                    sections.append("\n".join(current_section))
                    current_section = []
                current_section.append(f"\n{text}\n")
            else:
                current_section.append(text)
        
        if current_section:
            sections.append("\n".join(current_section))
        
        full_text = "\n\n".join(sections)
        full_text = clean_text(full_text)
        
        if full_text:
            pages.append({"page": 1, "text": full_text})
            
    except Exception as e:
        print(f"[DOCX Parse Error] {path}: {e}")
    return pages


def extract_tables_from_pdf(page):
    """Extract tables from PDF page for structured data."""
    tables = []
    try:
        tabs = page.find_tables()
        for table in tabs:
            if table and table.extract():
                tables.append(table.extract())
    except:
        pass
    return tables


def parse_manual_file(manual):
    """
    Parse the uploaded manual with improved structure preservation.
    """
    path = manual.file.path
    ext = os.path.splitext(path)[1].lower()
    pages = []

    if ext == ".pdf":
        pages = extract_text_from_pdf(path)
    elif ext in {".docx", ".doc"}:
        pages = extract_text_from_docx(path)
    else:
        print(f"[Parse Skipped] Unsupported format: {ext}")
        return

    if not pages:
        print(f"[Parse Warning] No text extracted from {manual.filename}")
        manual.processed = True
        manual.save()
        return

    # Save extracted text with metadata
    for p in pages:
        ManualText.objects.create(
            manual=manual,
            page_index=p["page"],
            text=p["text"]
        )

    manual.processed = True
    manual.save()
    print(f"[Parse Complete] {manual.filename} - {len(pages)} pages, "
          f"{sum(len(p['text']) for p in pages)} chars extracted.")