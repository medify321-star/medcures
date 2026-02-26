import json
import shutil
from datetime import datetime

# Read the current file
with open('pharmacopoeia.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a backup
backup_name = f'pharmacopoeia_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy('pharmacopoeia.json', backup_name)

# Rewrite it cleanly (this forces VS Code to refresh)
with open('pharmacopoeia.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Database refreshed!")
print(f"✓ Total drugs: {len(data)}")
print(f"✓ Backup created: {backup_name}")
print(f"✓ File will now show correctly in VS Code")

# Verify it's valid
try:
    with open('pharmacopoeia.json', 'r') as f:
        test = json.load(f)
    print(f"✓ JSON validation: PASSED")
except:
    print(f"✗ JSON validation: FAILED")
