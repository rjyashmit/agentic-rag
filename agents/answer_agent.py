from llm.ollama_llm import call_llm

def answer(context, question):
    prompt = f"""
Answer the question using ONLY the context below.
If not found, say "Not mentioned".

Context:
{context}

Question:
{question}
"""
    return call_llm(prompt)