import os
import uuid
import chromadb
from dotenv import load_dotenv

# Load env variables
load_dotenv()

CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT_ID")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "agentic_rag")

if not all([CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE]):
    raise ValueError("Chroma Cloud environment variables are missing")

# -----------------------------
# Chroma Cloud Client
# -----------------------------
client = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DATABASE
)

collection = client.get_or_create_collection(name=CHROMA_COLLECTION)

# -----------------------------
# Store embeddings
# -----------------------------
def store(chunks, embeddings):
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

# -----------------------------
# Search embeddings
# -----------------------------
def search(query_embedding, k=5):
# def search(query_embedding, k=2):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )