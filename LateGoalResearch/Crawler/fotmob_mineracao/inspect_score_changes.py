import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

shots = data["content"]["shotmap"]["shots"]

for shot in shots:

    if (
        "goal" in str(shot).lower()
        or shot.get("eventType") == "Goal"
    ):
        print(shot)
