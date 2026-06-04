import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

event_types = data["content"]["matchFacts"]["events"]["eventTypes"]

print(event_types)
