import requests
import json

url = "http://localhost:8001/chat"
data = {"question": "placements 2025"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=data, headers=headers)
    with open("api_res_utf8.log", "w", encoding="utf-8") as f:
        f.write(f"Status Code: {response.status_code}\n")
        f.write(f"Response Body: {json.dumps(response.json(), indent=2)}\n")
    print("Logged to api_res_utf8.log")
except Exception as e:
    print(f"Error: {e}")
