import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mf = data["content"]["matchFacts"]

for k, v in mf.items():

    print("\n" + "=" * 50)
    print(k)
    print(type(v))

    if isinstance(v, dict):
        print(v.keys())
