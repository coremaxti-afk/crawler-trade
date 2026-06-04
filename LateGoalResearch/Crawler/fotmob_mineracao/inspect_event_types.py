import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

shots = data["content"]["shotmap"]["shots"]

tipos = set()

for shot in shots:
    tipos.add(shot.get("eventType"))

print(sorted(tipos))
