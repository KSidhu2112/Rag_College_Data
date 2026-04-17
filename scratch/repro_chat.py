import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.prompts import PromptTemplate

load_dotenv(dotenv_path="backend/.env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
PERSIST_DIRECTORY = "backend/chroma_db"

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GOOGLE_API_KEY
)

vector_db = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings
)
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

QA_PROMPT = PromptTemplate(
    template="Use context: {context}\nQuestion: {question}", 
    input_variables=["context", "question"]
)

rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": QA_PROMPT}
)

try:
    print("Invoking chain...")
    response = rag_chain.invoke({"question": "What courses are offered?"})
    print("Success!")
    print(response["answer"])
except Exception as e:
    print(f"Failed: {e}")
