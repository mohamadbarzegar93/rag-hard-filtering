"""
Hard-filtering Retrieval approach: Mandatory metadata filter before vector search.
This is a direct improvement over the baselin in bas_line.py
Instead of searching the whole vector store, the filter restricts the candidate pool
by the provided metadata (e.g. provider, category, etc.)
"""


#Libraries
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"

def search(query, filters, k=5):
    #Running pure semantic search against the Chroma vector store, but
    #retricting it with a provided metadata filter.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db_chroma = Chroma(persist_directory = CHROMA_PATH, embedding_function=embeddings)
    return db_chroma.similarity_search_with_score(query, filter=filters, k=k)


if __name__ == "__main__":
    #Example query to test the RAG process
    query = "14-inch business laptop 16GB RAM"
    filters = {"provider": "BlitzMarkt"}
    results = search(query, filters, k=5)

    print(f"Query: {query}\n")
    for doc, score in results:
        print(f"[{doc.metadata['provider']}] {doc.page_content} (score={score:.4f})\n")
