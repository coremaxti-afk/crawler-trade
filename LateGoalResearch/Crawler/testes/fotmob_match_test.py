import requests

url = "https://www.fotmob.com/api/data/matchDetails?matchId=5190539"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)

print("Status:", r.status_code)
print(r.text[:500])
