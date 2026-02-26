import json

# Load and verify database
with open('pharmacopoeia.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Total drugs in file: {len(data)}")
print(f"✓ First drug: {data[0]['name']}")
print(f"✓ Last drug: {data[-1]['name']}")
print(f"\n✓ First 5 drugs:")
for i, drug in enumerate(data[0:5], 1):
    print(f"  {i}. {drug['name']} ({drug['category']})")

print(f"\n✓ Last 5 drugs:")
for i, drug in enumerate(data[-5:], len(data)-4):
    print(f"  {i}. {drug['name']} ({drug['category']})")

print(f"\n✓ Database ready! All {len(data)} drugs are saved.")
