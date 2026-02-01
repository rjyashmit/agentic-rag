from ingestion.embedder import model
from vectordb.chroma_client import search

# def retrieve(query):
#     q_emb = model.encode([query]).tolist()[0]
#     results = search(q_emb)
#     return results["documents"][0]


def retrieve(query):
    q_emb = model.encode([query], normalize_embeddings=True).tolist()[0]
    results = search(q_emb)

    # Limit context size
    docs = results["documents"][0][:1500]  # chars
    return docs