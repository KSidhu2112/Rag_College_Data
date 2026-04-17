import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("NVIDIA_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    response = requests.get("https://integrate.api.nvidia.com/v1/models", headers=headers)
    if response.status_code == 200:
        models = response.json().get("data", [])
        print("Available models:")
        for m in models:
            if "kimi" in m["id"].lower() or "deepseek" in m["id"].lower():
                print(f"- {m['id']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Failed: {e}")
