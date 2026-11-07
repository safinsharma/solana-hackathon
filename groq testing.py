import requests
import os

api_key = os.environ.get("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")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())