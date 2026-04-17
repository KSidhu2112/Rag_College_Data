import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def check_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        
        # Try a simple generation with 'gemini-1.5-flash-latest'
        model_name = 'gemini-1.5-flash'
        print(f"Testing model: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'API key is working!'")
        print(f"Success! API Response: {response.text}")
        return True
    except Exception as e:
        print(f"Error: API Key test failed: {str(e)}")
        return False

if __name__ == "__main__":
    check_api_key()
