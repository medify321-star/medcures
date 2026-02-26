import json
with open('backend/pharmacopoeia.json') as f:
    data = json.load(f)
    drug = data[0]
    print('Field names in first drug:')
    for key in list(drug.keys())[:4]:
        print(f'  {key}')
