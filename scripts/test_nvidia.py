import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="backend/.env")

nvidia_api_key = os.getenv("NVIDIA_API_KEY")
model_name = os.getenv("MODEL_NAME")

print(f"Testing NVIDIA NIM with model: {model_name}")

try:
    print("Initializing LLM...")
    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=nvidia_api_key,
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.3
    )
    
    print("Sending request...")
    response = llm.invoke("Hello, who are you?")
    print("\n--- Response Received ---")
    print(f"Content: {response.content}")
    print("-------------------------\n")
    print("Test successful!")
except Exception as e:
    print(f"\nTest failed with error type {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
