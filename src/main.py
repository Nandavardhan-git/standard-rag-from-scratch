from loaders.pdf_loader import extract_text_from_pdf
from preprocessors.text_cleaner import clean_text
from chunkers.text_chunker import chunk_text
from embeddings.embeddings_generator import generate_embeddings
try:
    pdf_text = extract_text_from_pdf("data/raw/pdf/Skill with People,10th ed-by Les Giblin.pdf")
    cleaned_text=clean_text(pdf_text)
    chunks=chunk_text(cleaned_text)
    embeddings=generate_embeddings(chunks)
    print(f"Total Chunks: {len(chunks)}")
    print(f"Embedding Shape: {embeddings.shape}")
except Exception as error:
    print(error)
