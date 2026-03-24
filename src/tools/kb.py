"""
Knowledge Base Tools — save and search your personal knowledge using RAG.
  - RecursiveCharacterTextSplitter: splits text into overlapping chunks
  - RAG pattern: store knowledge → retrieve relevant chunks → use in context
"""

import os
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


def _load_or_create_store():
    """
        Load existing FAISS index or return None.
    """
    index_path = os.path.join(KB_DIR, "index.faiss")
    if os.path.exists(index_path):
        return FAISS.load_local(KB_DIR, embeddings, allow_dangerous_deserialization=True)
    return None


@tool
def save_to_kb(text: str) -> str:
    """
        Save a piece of text to the knowledge base for later retrieval.
    """
    docs = splitter.create_documents([text])
    store = _load_or_create_store()
    
    if store:
        store.add_documents(docs)
    else:
        store = FAISS.from_documents(docs, embeddings)
    
    store.save_local(KB_DIR)
    return f"Saved {len(docs)} chunk(s) to knowledge base."


@tool 
def search_kb(query: str) -> str:
    """
        Search the knowledge base for information relevant to the query.
    """
    store = _load_or_create_store()
    
    if not store:
        return "Knowledge base is empty. Save something first!"
    
    results = store.similarity_search(query, k=3)
    
    if not results:
        return "No relevant results found."
    
    output = "**Found in Knowledge Base:**\n\n"
    for i, doc in enumerate(results, 1):
        output += f"{i}. {doc.page_content}\n\n"
    return output
