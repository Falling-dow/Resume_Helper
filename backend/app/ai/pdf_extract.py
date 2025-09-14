import os, subprocess, tempfile

def extract_text_from_pdf(pdf_path: str) -> str:
    """优先 pdfplumber → PyPDF2 → OCR 兜底。"""
    # A. pdfplumber
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for p in pdf.pages:
                t = p.extract_text() or ""
                pages.append(t.strip())
        text = "\n\n".join(p for p in pages if p)
        if len(text.strip()) > 30:
            return text.strip()
    except Exception:
        pass

    # B. PyPDF2
    try:
        import PyPDF2
        texts = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                t = page.extract_text() or ""
                texts.append(t.strip())
        text = "\n\n".join(texts)
        if len(text.strip()) > 30:
            return text.strip()
    except Exception:
        pass

    # C. OCR 兜底（需要 poppler + tesseract）
    try:
        from PIL import Image
        import pytesseract
        with tempfile.TemporaryDirectory() as td:
            out_prefix = os.path.join(td, "p")
            subprocess.run(["pdftoppm", "-png", pdf_path, out_prefix], check=True)
            ocr_pages = []
            for name in sorted(os.listdir(td)):
                if name.endswith(".png"):
                    img = Image.open(os.path.join(td, name))
                    ocr_pages.append(pytesseract.image_to_string(img))
        return "\n\n".join(ocr_pages).strip()
    except Exception:
        pass

    return ""
