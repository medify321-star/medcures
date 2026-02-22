import json
try:
    with open('pharmacopoeia.json', 'r') as f:
        data = json.load(f)
    print('✓ JSON loaded successfully')
    print(f'✓ Drugs found: {len(data.get("PharmacopoeiaDrugs", []))}')
except Exception as e:
    print(f'✗ Error: {e}')
