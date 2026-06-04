import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

momentum = data["content"]["momentum"]["main"]["data"]

print("Total registros:", len(momentum))

print("\nPrimeiro:")
print(momentum[0])

print("\nÚltimo:")
print(momentum[-1])
