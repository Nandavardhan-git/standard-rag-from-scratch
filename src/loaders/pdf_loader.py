import os
import pymupdf
def extract_text_from_pdf(pdf_path: str) -> str:
    if not pdf_path.endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"file not found : {pdf_path}")
    try:
        pages=[]
        with pymupdf.open(pdf_path) as document:
            for page in document:
                pages.append(page.get_text())
        return "".join(pages)
    except Exception as error:
        raise RuntimeError("Failed to read pdf ") from error
    
    
    
    
