
"""
Data indexing process for the RAG hard-filtering prototype.
"""

#Libraries
import glob
import json
import os


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DATA_PATH = os.path.join("data", "products", "*.json")
CHROMA_PATH = "chroma_db"


#------- Data Indexing Process -------
#Load all providers json catalog files and turning each product into a LangChain Document object. Then, we split the text into smaller chunks and store them in a Chroma vector database.

documents = []
for file in glob.glob(DATA_PATH):
    with open(file, "r", encoding="utf-8") as f:
        products = json.load(f)
        for product in products:
            # Description is what gets embedded
            page_content = f"{product['name']}. {product['description']}"
            #Extracting main metadatas for later hard-filtering
            metadata = {
                "product_id": product["product_id"],
                "provider": product["provider"],
                "category": product["category"],
                "region" : product["region"]
            }
            documents.append(Document(page_content=page_content, metadata= metadata))
print(f"Loaded {len(documents)} product documents from {DATA_PATH}.")
            

# Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                        chunk_overlap=50)
chunks = text_splitter.split_documents(documents)
print(f"Split into {len(documents)} chunks")

#Creating Embedding using a local model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print(f"Created embeddings for {len(documents)} chunks")

#Embedding the chinks as vectors and loading them into the database
db_chroma = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
print(f"{len(documents)} chunks stored into Chroma database at {CHROMA_PATH}.")
