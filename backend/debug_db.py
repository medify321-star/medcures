import json

with open('pharmacopoeia.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
print(f"Data is a: {type(data)}")

# Check first 5 entries
for i, entry in enumerate(data[:5]):
    print(f"\nEntry {i}: type={type(entry)}")
    if isinstance(entry, dict):
        print(f"  Keys: {list(entry.keys())}")
        if entry:
            print(f"  First key value: {list(entry.values())[0]}")
    else:
        print(f"  Value: {entry}")
