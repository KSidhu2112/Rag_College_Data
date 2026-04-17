import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("GOOGLE_API_KEY")

print("Testing LangChain Google AI Embeddings...")
model_name = "gemini-embedding-001"
print(f"Testing with model: {model_name}")

try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=api_key
    )
    result = embeddings.embed_query("Hello world")
    print(f"Success! Vector length: {len(result)}")
except Exception as e:
    print(f"Error: {e}")

model_name_2 = "models/gemini-embedding-001"
print(f"Testing with model: {model_name_2}")
try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model=model_name_2,
        google_api_key=api_key
    )
    result = embeddings.embed_query("Hello world")
    print(f"Success! Vector length: {len(result)}")
except Exception as e:
    print(f"Error: {e}")
