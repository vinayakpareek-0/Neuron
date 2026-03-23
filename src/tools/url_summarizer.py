"""
URL Summarizer Tool — loads a webpage and summarizes its content.
  - @tool decorator: turns any Python function into an agent-usable tool
  - WebBaseLoader: a Document Loader that fetches HTML and converts to text
  - load_summarize_chain: a pre-built Chain that summarizes a list of documents
"""

from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from src.config import llm

@tool 
def summarize_url(url:str)->str:
    """Fetch a webpage and return a concise summary of its content. Input should be a valid URL."""
    loader = WebBaseLoader(url)
    docs = loader.load()

    # to stay under limit for groq free tier
    for doc in docs:
        if len(doc.page_content) > 2000:
            doc.page_content = doc.page_content[:2000]


    chain = load_summarize_chain(llm , chain_type="stuff") 
    # "stuff" strategy = shoves all docs into one prompt,(Good for short pages)
    result = chain.invoke(docs)
    return result["output_text"]
