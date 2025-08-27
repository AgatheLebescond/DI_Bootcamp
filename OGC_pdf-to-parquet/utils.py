import base64
import io
import time
from typing import List, Tuple, Dict, Any

import fitz  # PyMuPDF
from PIL import Image
from pdfminer.high_level import extract_text
from langdetect import detect


def render_pdf_page_to_image_bytes(pdf_path: str, page_index: int, zoom: float = 1.5) -> bytes:
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_index)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img_bytes = pix.tobytes("png")
    doc.close()
    return img_bytes


def extract_text_from_pdf(pdf_path: str) -> List[str]:
    pages_text: List[str] = []
    doc = fitz.open(pdf_path)
    for idx in range(len(doc)):
        text = doc.load_page(idx).get_text("text")
        if not text:
            # fallback pdfminer
            text = extract_text(pdf_path) or ""
        pages_text.append(text)
    doc.close()
    return pages_text


def detect_language_from_pages(pages_text: List[str]) -> str:
    concatenated = "\n".join(pages_text[:5]) or "English"
    try:
        return detect(concatenated)
    except Exception:
        return "en"


def image_bytes_to_b64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode("utf-8")
