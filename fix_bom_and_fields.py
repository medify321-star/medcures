#!/usr/bin/env python3
"""
FINAL FIX - Handle BOM and convert field names to lowercase
"""
import sys
from pathlib import Path
sys.path.insert(0, str((Path(__file__).parent / 'backend').resolve()))
from schema_utils import load_drugs, save_drugs

file_path = Path('backend/pharmacopoeia.json')
drugs = load_drugs(file_path)
save_drugs(drugs, file_path)

print(f"\n✅ FIXED!")
print(f"Total drugs: {len(drugs)}")
print(f"Field names: {list(drugs[0].keys())}")
print(f"File size: {file_path.stat().st_size:,} bytes")
print(f"\nFirst drug sample:")
print(f"  name: {drugs[0]['name']}")
print(f"  category: {drugs[0]['category']}")
print(f"  route: {drugs[0]['route']}")
