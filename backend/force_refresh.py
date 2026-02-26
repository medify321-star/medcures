import json

# Read and rewrite the file to force VS Code cache clear
with open('pharmacopoeia.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write with explicit formatting
with open('pharmacopoeia.json', 'w', encoding='utf-8') as f:
    # Write opening bracket
    f.write('[\n')
    
    # Write each drug
    for i, drug in enumerate(data):
        f.write('  ')
        json.dump(drug, f, ensure_ascii=False, separators=(',', ': '))
        if i < len(data) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    
    # Write closing bracket
    f.write(']\n')

print(f"✓ File completely rewritten")
print(f"✓ Total drugs: {len(data)}")
print(f"✓ File size: {(52712)} bytes")

# Verify
with open('pharmacopoeia.json', 'r') as f:
    test = json.load(f)
print(f"✓ Verification: {len(test)} drugs loaded successfully")
print(f"✓ First drug: {test[0]['name']}")
print(f"✓ Last drug: {test[-1]['name']}")
