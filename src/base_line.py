""""
This is a base line for prompting and RAG using semantic search without filtering.

This is a comparison point for the hard-filtering approach, 
which is implemented in the hard_filter.py file.

That's how it works:
1. A query is defined to test the RAG process.
2. The query is used to retrieve the top 5 most relevant chunks from the Chroma vector database.
3. The retrieved chunks are then used to generate an answer based on the query using
    a local LLM model.

"""

#Libraries
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"

def search(query, k=5):
    #Running pure semantic search against the Chroma vector store.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db_chroma = Chroma(persist_directory = CHROMA_PATH, embedding_function=embeddings)
    return db_chroma.similarity_search_with_score(query, k=k)


if __name__ == "__main__":
    #Example query to test the RAG process
    query = "14-inch business laptop 16GB RAM"
    results = search(query, k=5)

    print(f"Query: {query}\n")
    for doc, score in results:
        print(f"[{doc.metadata['provider']}] {doc.page_content} (score={score:.4f})\n")
