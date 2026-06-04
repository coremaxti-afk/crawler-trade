import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

stats = data["content"]["stats"]["Periods"]["All"]["stats"]

for grupo in stats:
    print("\nGRUPO:", grupo["title"])

    for item in grupo["stats"]:
        print("-", item.get("title"))
