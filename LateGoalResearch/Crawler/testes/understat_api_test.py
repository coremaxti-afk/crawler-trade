import requests

url = "https://understat.com/getLeagueData/EPL/2024"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://understat.com/league/EPL/2024"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(response.text[:1000])
