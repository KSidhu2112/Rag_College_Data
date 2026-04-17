import os
import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain imports
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_mongodb import MongoDBChatMessageHistory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI(title="LearnHub College Chatbot API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PROVIDER = os.getenv("PROVIDER", "groq").lower()
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
# EMBEDDING_MODEL now defaults to a stable local model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "learnhub_db"
COLLECTION_NAME = "chat_history"

# Initialize Embeddings (HuggingFace is more stable and free)
try:
    logger.info(f"Initializing stable local embeddings: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    logger.info("Embeddings initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing embeddings: {e}")
    embeddings = None

# Initialize LLM
def get_llm():
    try:
        if PROVIDER == "groq":
            return ChatGroq(
                model=MODEL_NAME,
                groq_api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.3
            )
        elif PROVIDER == "openai":
            return ChatOpenAI(
                model=MODEL_NAME or "gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.3
            )
        elif PROVIDER == "anthropic":
            return ChatAnthropic(
                model=MODEL_NAME or "claude-3-5-sonnet-20240620",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=0.3
            )
        else: # Default to Google
            return ChatGoogleGenerativeAI(
                model=MODEL_NAME or "gemini-1.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.3
            )
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        return None

llm = get_llm()

# Load Vector DB
def load_vector_db():
    if not embeddings:
        logger.error("Embeddings not initialized, cannot load FAISS.")
        return None
    
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            logger.info(f"Loading FAISS index from {FAISS_INDEX_PATH}")
            return FAISS.load_local(
                FAISS_INDEX_PATH, 
                embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            logger.error(f"Error loading FAISS index: {e}")
            logger.warning("The FAISS index might be incompatible with the current embedding model. Please run ingest.py again.")
            return None
    else:
        logger.warning(f"FAISS index not found at {FAISS_INDEX_PATH}")
        return None

vector_db = load_vector_db()

# Chat Memory with MongoDB
def get_chat_history(session_id: str = "default_user"):
    return MongoDBChatMessageHistory(
        connection_string=MONGO_URI,
        session_id=session_id,
        database_name=DB_NAME,
        collection_name=COLLECTION_NAME,
    )

memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=get_chat_history(),
    return_messages=True,
    output_key="answer"
)

# Custom Prompt
QA_PROMPT_TEMPLATE = """You are a helpful and professional college assistant for "LearnHub College". 
Use the following pieces of retrieved context to answer the user's question.
If the context doesn't contain the answer, politely say that you don't know based on the available records, but don't try to make up an answer.
Keep the answer concise and relevant.

Context:
{context}

Question: {question}

Helpful Answer:"""

QA_PROMPT = PromptTemplate(
    template=QA_PROMPT_TEMPLATE, 
    input_variables=["context", "question"]
)

# RAG Chain
def get_rag_chain():
    if vector_db and llm:
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_db.as_retriever(search_kwargs={"k": 5}),
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT}
        )
    return None

rag_chain = get_rag_chain()

class Query(BaseModel):
    question: str
    session_id: str = "default_user"

@app.get("/")
def read_root():
    return {"message": "Welcome to LearnHub Chatbot API - Status: ONLINE"}

@app.get("/history")
async def get_history(session_id: str = "default_user"):
    try:
        history = get_chat_history(session_id)
        messages = history.messages
        chat_history = []
        for msg in messages:
            chat_history.append({
                "role": "user" if msg.type == "human" else "assistant",
                "content": msg.content
            })
        return {"history": chat_history}
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return {"history": []}

@app.get("/sessions")
async def get_sessions():
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Get unique session IDs
        sessions = collection.distinct("SessionId")
        
        # For each session, get the last message or first message to use as a label
        session_list = []
        for s_id in sessions[::-1]: # Reverse to get latest first
            # Get first message doc
            first_msg = collection.find_one({"SessionId": s_id}, sort=[("_id", 1)])
            label = "Untitled Chat"
            if first_msg and "History" in first_msg:
                import json
                try:
                    history_data = json.loads(first_msg["History"])
                    content = history_data.get("data", {}).get("content", "")
                    if content:
                        label = content[:30] + "..." if len(content) > 30 else content
                except:
                    pass
            
            session_list.append({"id": s_id, "label": label})
            
        return {"sessions": session_list[:10]} # Return last 10
    except Exception as e:
        logger.error(f"Error fetching sessions: {e}")
        return {"sessions": []}

@app.post("/chat")
async def chat(query: Query):
    global vector_db
    
    # Initialize session-specific memory
    session_memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=get_chat_history(query.session_id),
        return_messages=True,
        output_key="answer"
    )

    # Build a session-specific RAG chain
    if not vector_db:
         vector_db = load_vector_db()
    
    if not vector_db or not llm:
        logger.error("RAG components not properly initialized")
        raise HTTPException(status_code=503, detail="RAG system components missing")

    session_rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_db.as_retriever(search_kwargs={"k": 5}),
        memory=session_memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT}
    )
    
    try:
        logger.info(f"Processing query for session {query.session_id}: {query.question}")
        # Run the chain
        response = session_rag_chain.invoke({"question": query.question})
        
        # Extract sources from documents
        sources = []
        unique_sources = set()
        for doc in response.get("source_documents", []):
            source_path = doc.metadata.get("source", "Unknown")
            source_name = os.path.basename(str(source_path))
            page_info = doc.metadata.get("page", "N/A")
            
            source_key = f"{source_name}_{page_info}"
            if source_key not in unique_sources:
                sources.append({
                    "source": source_name,
                    "page": page_info
                })
                unique_sources.add(source_key)
            
        return {
            "answer": response["answer"],
            "sources": sources[:3] 
        }
    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    logger.info(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
