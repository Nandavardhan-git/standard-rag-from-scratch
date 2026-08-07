from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
def generate_embeddings(chunks):
    return model.encode(chunks)
def generate_query_embedding(query):
    return model.encode(query)

