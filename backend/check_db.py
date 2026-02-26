import json

with open("pharmacopoeia.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"Total drugs in database: {len(data)}")
    if data:
        print(f"First drug: {data[0]['Drug']}")
        print(f"Last drug: {data[-1]['Drug']}")
