import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

with open("available_models.txt", "w", encoding="utf-8") as f:
    f.write("Available Models:\n")
    try:
        for m in genai.list_models():
            f.write(f"{m.name} - {m.supported_generation_methods}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
