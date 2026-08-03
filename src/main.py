from loaders.pdf_loader import extract_text_from_pdf
from preprocessors.text_cleaner import clean_text
try:
    pdf_text = extract_text_from_pdf("data/raw/pdf/Skill with People,10th ed-by Les Giblin.pdf")
    cleaned_text=clean_text(pdf_text)
    print(cleaned_text[:3000])
except Exception as error:
    print(error)
