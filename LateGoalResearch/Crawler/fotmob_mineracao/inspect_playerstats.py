import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

player_id = list(data["content"]["playerStats"].keys())[0]

print("PLAYER:", player_id)

obj = data["content"]["playerStats"][player_id]

print(type(obj))

if isinstance(obj, dict):
    print(obj.keys())
