from chromadb import PersistentClient
client=PersistentClient(
    path="database"
)
collection=client.get_or_create_collection(
    name="rag_collection"
)
collection = client.get_or_create_collection(
    name="rag_collection"
)

print("Stored chunks:", collection.count())
def reset_collection():
    global collection
    client.delete_collection("rag_collection")
    collection = client.get_or_create_collection(
        name="rag_collection"
    )
def add_documents(chunks,embeddings):
    reset_collection()
    ids=[
        f"chunk_{i}" for i in range(len(chunks))
    ]
    metadatas = [
    {"chunk_index": i}
    for i in range(len(chunks))
    ]
    embeddings = embeddings.tolist()
    collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
    )
def retrieve(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    return results    
