import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Testing embedding models...")
models_to_test = ["models/gemini-embedding-001", "models/gemini-embedding-2-preview", "gemini-embedding-001"]

for m in models_to_test:
    try:
        print(f"Testing {m}...")
        genai.embed_content(model=m, content="Hello world")
        print(f"Success with {m}!")
    except Exception as e:
        print(f"Failed with {m}: {e}")
