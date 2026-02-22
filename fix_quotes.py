import json

file_path = r'c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent\backend\pharmacopoeia.json'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace curly quotes with regular dashes for numeric ranges
content = content.replace('"', '-')  # Both left and right curly double quotes
content = content.replace('"', '-')  
content = content.replace("'", "'")  # Single quotes to apostrophe
content = content.replace("'", "'")

# Parse JSON to validate
try:
    data = json.loads(content)
    #  Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Successfully fixed pharmacopoeia.json')
except json.JSONDecodeError as e:
    print(f'JSON error: {e}')
