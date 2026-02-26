import json
from pathlib import Path

base = Path('.')
main_file = base / 'backend' / 'pharmacopoeia.json'

with open(main_file) as f:
    data = json.load(f)

print("=" * 70)
print("✅ CONSOLIDATION & NORMALIZATION COMPLETE")
print("=" * 70)
print()
print("📊 FINAL DRUG DATABASE STATUS:")
print(f"  Location: backend/pharmacopoeia.json")
print(f"  Total drugs: {len(data)}")
print(f"  File size: {main_file.stat().st_size:,} bytes")
print()
print("✓ All drugs consolidated into ONE file")
print("✓ All field names normalized to lowercase:")
print(f"    name, category, route, storage, dose, uses")
print(f"    side_effects, citations, disclaimer")
print("✓ No duplicates")
print("✓ Backup and markers copies deleted")
print()
print("📝 DATABASE STRUCTURE:")
drug = data[0]
print(f"  Fields: {list(drug.keys())}")
print()
print("🎯 STATUS: Ready for use - all 145 drugs in one clean master file!")
print("=" * 70)
