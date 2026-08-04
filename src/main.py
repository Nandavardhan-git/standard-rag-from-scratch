from loaders.pdf_loader import extract_text_from_pdf
from preprocessors.text_cleaner import clean_text
from chunkers.text_chunker import chunk_text
try:
    pdf_text = extract_text_from_pdf("data/raw/pdf/Skill with People,10th ed-by Les Giblin.pdf")
    cleaned_text=clean_text(pdf_text)
    chunks=chunk_text(cleaned_text)
    print("Total Chunks:", len(chunks))
    print("\n========== Chunk 1 ==========\n")
    print(chunks[0])
    print("\n========== Chunk 2 ==========\n")
    print(chunks[1])
except Exception as error:
    print(error)
