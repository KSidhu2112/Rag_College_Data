import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("GOOGLE_API_KEY")

print("Testing ChatGoogleGenerativeAI...")
# Try different forms of gemini-1.5-flash
models = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-1.5-flash-latest"]

for m in models:
    try:
        print(f"\nTesting {m}...")
        llm = ChatGoogleGenerativeAI(model=m, google_api_key=api_key)
        res = llm.invoke("Hello")
        print(f"Success with {m}: {res.content}")
    except Exception as e:
        print(f"Failed with {m}: {e}")
