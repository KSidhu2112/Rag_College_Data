import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("NVIDIA_API_KEY")
model = os.getenv("MODEL_NAME")

print(f"Testing model: {model}")
print(f"API Key: {api_key[:10]}...")

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": model,
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.5,
    "top_p": 1,
    "max_tokens": 1024,
    "stream": False
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json()['choices'][0]['message']['content'])
    else:
        print("Error Response:", response.text)
except Exception as e:
    print(f"Exception: {e}")
