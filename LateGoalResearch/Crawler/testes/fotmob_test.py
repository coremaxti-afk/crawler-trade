import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.fotmob.com"

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.text[:300])
