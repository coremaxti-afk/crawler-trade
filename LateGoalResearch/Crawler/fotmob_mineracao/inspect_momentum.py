import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

momentum = data["content"]["momentum"]

print(type(momentum))
print()

if isinstance(momentum, dict):
    print(momentum.keys())

print()
print(str(momentum)[:2000])
