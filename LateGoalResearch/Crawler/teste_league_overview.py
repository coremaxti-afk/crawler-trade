import requests
import json

url = "https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025"

data = requests.get(url).json()

print(data.keys())

print("\nQuantidade de jogos:")
print(len(data["overview"]["leagueOverviewMatches"]))

print("\nPrimeiro jogo:")
print(json.dumps(
    data["overview"]["leagueOverviewMatches"][0],
    indent=2,
    ensure_ascii=False
))
