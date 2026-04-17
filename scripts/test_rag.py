import os
import traceback
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

# Load environment variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(ROOT_DIR), "backend", ".env"))

PROVIDER = "google"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
FAISS_INDEX_PATH = os.path.join(os.path.dirname(ROOT_DIR), "backend", "faiss_index")

print(f"Testing with: LLM={MODEL_NAME}, Embedding={EMBEDDING_MODEL}")

try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

    print(f"Loading FAISS index from {FAISS_INDEX_PATH}...")
    vector_db = FAISS.load_local(
        FAISS_INDEX_PATH, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    print("FAISS index loaded successfully.")
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

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

    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT}
    )

    print("Running query: 'placements'")
    response = rag_chain.invoke({"question": "placements"})
    print("Answer:")
    print(response["answer"])

except Exception as e:
    print("Error occurred!")
    with open("rag_trace.txt", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
    print("Trace written to rag_trace.txt")
