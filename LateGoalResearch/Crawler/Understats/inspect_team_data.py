import requests
import json

url = "https://understat.com/getLeagueData/EPL/2024"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://understat.com/league/EPL/2024"
}

response = requests.post(url, headers=headers)

data = response.json()

first_team = list(data["teams"].keys())[0]

print("ID:", first_team)

print(
    json.dumps(
        data["teams"][first_team],
        indent=2
    )[:3000]
)
