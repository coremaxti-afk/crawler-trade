import json

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for key in data["content"]:
    print("\n" + "="*50)
    print(key)

    try:
        value = data["content"][key]

        if isinstance(value, dict):
            print("dict")
            print(value.keys())

        elif isinstance(value, list):
            print("list")
            print("itens:", len(value))

        else:
            print(type(value))

    except Exception as e:
        print(e)
