import requests
import json

url = "https://understat.com/getLeagueData/EPL/2024"

response = requests.post(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://understat.com/league/EPL/2024"
    }
)

data = response.json()

print(type(data["dates"]))

print("Quantidade de registros:", len(data["dates"]))

print("\nPrimeiro registro:\n")

print(json.dumps(data["dates"][0], indent=2))
