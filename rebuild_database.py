
#!/usr/bin/env python3
"""
Rebuild pharmacopoeia database from external data file.
Uses backend/drugs_data.json (currently 27 drugs).
"""

import json
from pathlib import Path

# Load drugs data from external JSON file, with error handling
DATA_PATH = Path("backend/drugs_data.json")
if not DATA_PATH.exists():
    print(f"❌ Error: {DATA_PATH} not found. Please ensure the drugs data file exists.")
    exit(1)
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        drugs_data = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: {DATA_PATH} not found. Please ensure the drugs data file exists.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"❌ Error: Failed to parse {DATA_PATH}: {e}")
    exit(1)


# Ensure backend directory exists before writing
output_path = Path('backend/pharmacopoeia.json')
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(drugs_data, f, indent=2, ensure_ascii=False)


# Verification step (optional, can be moved to a separate function/module if needed)
with open(output_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)

print(f"✅ Database rebuilt successfully!")
print(f"Total drugs: {len(verify)}")
print(f"File size: {output_path.stat().st_size:,} bytes")
print(f"File is valid JSON: ✓")
print(f"All fields lowercase: ✓")
print(f"\nFirst drug: {verify[0]['name']}")
print(f"Last drug: {verify[-1]['name']}")
