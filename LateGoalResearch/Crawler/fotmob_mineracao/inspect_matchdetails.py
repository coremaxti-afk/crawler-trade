import json

with open(
    "matchdetails.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

print("\nCHAVES PRINCIPAIS:")
print(data.keys())

print("\nCONTENT:")
print(data["content"].keys())
