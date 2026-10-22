from embeddings.embeddings_generator import generate_query_embedding
from vector_store.chroma_store import retrieve
from llm.prompt_builder import build_prompt
from llm.gemini_client import generate_response

while True:
    query = input("\nAsk a question: ")
    if query.lower() == "exit":
        break
    query_embedding = generate_query_embedding(query)
    results = retrieve(query_embedding)
    documents = results["documents"][0]
    context = "\n\n".join(documents)
    prompt = build_prompt(context, query)
    answer = generate_response(prompt)
    print("\nAnswer:")
    print(answer)