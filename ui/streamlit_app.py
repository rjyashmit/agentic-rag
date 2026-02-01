import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from ingestion.loader import load_document
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_text
from vectordb.chroma_client import store
from app import ask

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="Agentic RAG",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f172a;
}

.sidebar-title {
    color: white;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 5px;
}

.sidebar-subtitle {
    color: #cbd5f5;
    font-size: 13px;
    margin-bottom: 30px;
}

/* Section title */
.section-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
}

/* Upload card */
.upload-card {
    border: 2px dashed #3b82f6;
    border-radius: 16px;
    padding: 50px;
    text-align: center;
    background: linear-gradient(145deg, #f8fbff, #eef4ff);
    margin-top: 20px;
}

/* Upload icon */
.upload-icon {
    font-size: 60px;
}

/* Upload text */
.upload-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 15px;
}

.upload-sub {
    color: #64748b;
    font-size: 14px;
    margin-top: 8px;
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    padding: 12px 22px;
    font-weight: 700;
    background: linear-gradient(to right, #2563eb, #3b82f6);
    color: white;
    border: none;
}

/* Input */
.stTextInput input {
    border-radius: 10px;
    padding: 12px;
}

/* Answer box */
.answer-box {
    background-color: #0f172a;;
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Agentic RAG</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">AI-powered document intelligence</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📤 Upload & Index", "💬 Ask Questions"],
        label_visibility="collapsed"
    )

if page == "📤 Upload & Index":

    st.markdown('<div class="section-title">Upload Documents</div>', unsafe_allow_html=True)
    st.write("Upload your files and let AI agents index them for intelligent search.")

    st.markdown("""
    <div class="upload-card">
        <div class="upload-icon">⬆️</div>
        <div class="upload-title">Drop files here or click to upload</div>
        <div class="upload-sub">
            PDF, DOCX, PPTX, XLSX, TXT<br>
            Max size: 200MB per file
        </div>
    </div>
    """, unsafe_allow_html=True)

    files = st.file_uploader(
        "",
        type=["pdf", "docx", "pptx", "xlsx", "txt"],
        accept_multiple_files=True
    )

    if st.button("🚀 Process & Index Documents"):
        if not files:
            st.warning("Please upload at least one document.")
        else:
            with st.spinner("Processing and indexing documents..."):
                for f in files:
                    path = os.path.join(UPLOAD_DIR, f.name)
                    with open(path, "wb") as file:
                        file.write(f.read())

                    text = load_document(path)
                    chunks = chunk_text(text)
                    embeddings = embed_text(chunks)
                    store(chunks, embeddings)

            st.success("✅ Documents indexed successfully!")

if page == "💬 Ask Questions":

    st.markdown('<div class="section-title">Ask Your Documents</div>', unsafe_allow_html=True)
    st.write("Ask natural language questions and get precise answers.")

    query = st.text_input(
        "Your question",
        placeholder="e.g. What are the key terms mentioned in the contract?"
    )

    if st.button("🤖 Get Answer"):
        if not query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI agents are reasoning..."):
                result = ask(query)

            st.markdown("### 📌 Answer")
            st.markdown(f'<div class="answer-box">{result}</div>', unsafe_allow_html=True)