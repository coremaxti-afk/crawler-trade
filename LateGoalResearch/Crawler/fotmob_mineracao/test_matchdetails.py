import requests

url = "https://www.fotmob.com/api/data/matchDetails?matchId=4506263"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.fotmob.com/",
    "Accept": "application/json"
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print(response.status_code)
print(response.text[:200])
