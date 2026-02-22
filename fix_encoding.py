import json

file_path = r'c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent\backend\pharmacopoeia.json'
with open(file_path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix all the corrupted characters with proper replacements
content = content.replace('"', '-')  # Replace broken quote-like chars with dash
content = content.replace("'", "'")  # Smart quotes to regular apostrophe

# Parse and re-serialize to ensure valid JSON
data = json.loads(content)
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    
print('Fixed encoding in pharmacopoeia.json')
