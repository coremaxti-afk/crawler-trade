import requests

url = "https://www.fotmob.com/api/data/matchDetails?matchId=4506263"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36 Edg/148.0.0.0",
    "Referer": "https://www.fotmob.com/pt-BR/matches/fulham-vs-manchester-united/3cqww9",
    "x-mas": "eyJib2R5Ijp7InVybCI6Ii9hcGkvZGF0YS9tYXRjaERldGFpbHM/bWF0Y2hJZD00NTA2MjYzIiwiY29kZSI6MTc4MDQxNTA5NjcxNywiZm9vIjoicHJvZHVjdGlvbjpjNDMxZmEyYTE4ZjMxNGI2MTk4NTQwMjVhMTk5MDkyYzBhY2NiNmFjIn0sInNpZ25hdHVyZSI6IjM4NzlDMkNGQjM1MkM4Q0U5QTFEMkY5NkEzNDY5OTNFIn0="
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Status:", response.status_code)
print(response.text[:500])
