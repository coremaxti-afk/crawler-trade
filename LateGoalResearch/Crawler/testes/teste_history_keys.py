import requests
import json

url = "https://understat.com/getLeagueData/EPL/2024"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://understat.com/league/EPL/2024"
}

data = requests.post(url, headers=headers).json()

team_id = list(data["teams"].keys())[0]

history = data["teams"][team_id]["history"][0]

print(history.keys())
