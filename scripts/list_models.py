import os
import google.generativeai as genai
from dotenv import load_dotenv

# Search for .env in current or parent directory
load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Listing models...")
try:
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(f"Embedding model: {m.name}")
        if 'generateContent' in m.supported_generation_methods:
            print(f"Generation model: {m.name}")
except Exception as e:
    print(f"Error: {e}")
