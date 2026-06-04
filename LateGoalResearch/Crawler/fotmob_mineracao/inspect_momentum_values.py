import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

momentum = data["content"]["momentum"]["main"]["data"]

for item in momentum[:15]:
    print(item)
