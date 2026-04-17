import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

FAISS_INDEX_PATH = "backend/faiss_index"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def verify_faiss():
    if not os.path.exists(FAISS_INDEX_PATH):
        print(f"Error: FAISS index not found at {FAISS_INDEX_PATH}")
        return

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )

    print(f"Loading FAISS index from {FAISS_INDEX_PATH}...")
    vector_db = FAISS.load_local(
        FAISS_INDEX_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # Check index size
    # FAISS index is stored in vector_db.index
    count = vector_db.index.ntotal
    print(f"Success! FAISS index contains {count} vectors.")

if __name__ == "__main__":
    verify_faiss()
