import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.fotmob.com/api/leagues?id=47"

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("\nChaves principais:")
    print(data.keys())
