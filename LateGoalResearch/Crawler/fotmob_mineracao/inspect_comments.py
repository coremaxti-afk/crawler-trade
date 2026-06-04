import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

events = data["content"]["matchFacts"]["events"]["events"]

for event in events:

    if event["type"] == "Comment":

        print()
        print("=" * 50)
        print(event)
