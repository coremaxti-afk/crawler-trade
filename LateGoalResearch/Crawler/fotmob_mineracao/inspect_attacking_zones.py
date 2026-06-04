import json
from pprint import pprint

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pprint(data["content"]["attackingZones"])
