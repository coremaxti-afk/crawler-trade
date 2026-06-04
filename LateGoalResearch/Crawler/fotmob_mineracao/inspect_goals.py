import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

shots = data["content"]["shotmap"]["shots"]

for shot in shots:
    if shot.get("eventType") == "Goal":
        print()
        print("MIN:", shot.get("min"))
        print("ADDED:", shot.get("minAdded"))
        print("TEAM:", shot.get("teamId"))
        print("PLAYER:", shot.get("playerName"))
        print("XG:", shot.get("expectedGoals"))
