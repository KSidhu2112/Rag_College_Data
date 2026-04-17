import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env")) # Check root .env
if not os.path.exists(os.path.join(BASE_DIR, "backend", ".env")):
     load_dotenv(dotenv_path=os.path.join(BASE_DIR, "backend", ".env")) # Fallback

PROVIDER = os.getenv("PROVIDER", "groq").lower()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Default to stable local embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "backend", "faiss_index")
DATA_DIRECTORY = os.path.join(BASE_DIR, "data")

def ingest_data():
    print(f"--- LearnHub Data Ingestion ---")
    print(f"Data Directory: {DATA_DIRECTORY}")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    
    # Check if data directory exists
    if not os.path.exists(DATA_DIRECTORY):
        print(f"Error: {DATA_DIRECTORY} not found!")
        return

    # Load different types of files
    print("Loading documents...")
    loaders = [
        DirectoryLoader(DATA_DIRECTORY, glob="**/*.pdf", loader_cls=PyPDFLoader),
        DirectoryLoader(DATA_DIRECTORY, glob="**/*.csv", loader_cls=CSVLoader),
        DirectoryLoader(DATA_DIRECTORY, glob="**/*.txt", loader_cls=TextLoader),
    ]

    documents = []
    for loader in loaders:
        try:
            docs = loader.load()
            if docs:
                documents.extend(docs)
                print(f"  - Loaded {len(docs)} files from {loader.glob}")
        except Exception as e:
            print(f"  - Warning during loading: {e}")

    if not documents:
        print("No documents found in the data directory!")
        return

    print(f"Total: {len(documents)} documents loaded.")

    # Split documents into chunks
    print("Chunking documents (size=1000, overlap=200)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Generated {len(chunks)} chunks.")

    # Generate embeddings
    print(f"Generating embeddings using {EMBEDDING_MODEL}...")
    try:
        # Use HuggingFace for stability as requested
        if "sentence-transformers" in EMBEDDING_MODEL or "all-MiniLM" in EMBEDDING_MODEL:
            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        elif PROVIDER == "openai":
            embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
        else: # Google default
            embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)
            
        print("Creating and saving FAISS index...")
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(FAISS_INDEX_PATH)
        print(f"SUCCESS: FAISS index saved to {FAISS_INDEX_PATH}")
        
    except Exception as e:
        print(f"CRITICAL ERROR during ingestion: {e}")

if __name__ == "__main__":
    ingest_data()
