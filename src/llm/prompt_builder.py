def build_prompt(context, question):
    prompt = f"""
You are a helpful assistant answering questions about a document.
Use the provided context to answer the user's question.
You may summarize or reasonably infer the answer from the information
contained in the context.
If the context genuinely does not contain enough information,
say that the information is not available in the provided context.
Context:
{context}
Question:
{question}
Answer:
"""
    return prompt