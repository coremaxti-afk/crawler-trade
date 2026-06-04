import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

events = data["content"]["matchFacts"]["events"]

print(type(events))

if isinstance(events, list):
    print("Quantidade:", len(events))

    if len(events):
        print()
        print(events[0])

elif isinstance(events, dict):
    print(events.keys())

    for key in events:
        print("\n=== ", key, " ===")

        value = events[key]

        if isinstance(value, list):
            print("Itens:", len(value))

            if len(value):
                print(value[0])

        else:
            print(type(value))
