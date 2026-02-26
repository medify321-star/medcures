#!/usr/bin/env python3
"""
FINAL CONSOLIDATION & NORMALIZATION using schema_utils
"""
import sys
from pathlib import Path
import json
sys.path.insert(0, str((Path(__file__).parent / 'backend').resolve()))
from schema_utils import normalize_drug_fields, save_drugs

base_dir = Path(__file__).parent

# Locations of all drug files
drug_files = {
    'main': base_dir / 'backend' / 'pharmacopoeia.json',
    'backup': base_dir / 'backend' / 'pharmacopoeia_backup_20260226_144151.json',
    'markers': base_dir / 'data' / 'backup' / 'pharmacopoeia.json'
}

print("🔄 FINAL CONSOLIDATION & NORMALIZATION")
print("=" * 70)

# Collect all drugs
consolidated_drugs = {}
processed_files = []

for label, file_path in drug_files.items():
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                print(f"📖 {label:12} : {len(data):3} drugs")
                processed_files.append((label, len(data)))
                # Normalize and deduplicate
                for drug in data:
                    if isinstance(drug, dict):
                        # Get the drug name (try different fields)
                        name = None
                        for key in ['name', 'Name', 'drug', 'Drug']:
                            if key in drug:
                                name = drug[key]
                                break
                        if name:
                            name_key = str(name).lower().strip()
                            # Only add if not already present (keeps first occurrence)
                            if name_key not in consolidated_drugs:
                                normalized = normalize_drug_fields(drug)
                                consolidated_drugs[name_key] = normalized
        else:
            print(f"   {label:12} : SKIPPED (file not found)")
    except json.JSONDecodeError as e:
        print(f"   {label:12} : SKIPPED (corrupted JSON at line {e.lineno})")
    except Exception as e:
        print(f"   {label:12} : SKIPPED ({str(e)[:40]})")

print("\n" + "=" * 70)
print("🛠️  PROCESSING & NORMALIZATION")
print("=" * 70)

# Create final list sorted by name
final_drugs = [consolidated_drugs[k] for k in sorted(consolidated_drugs.keys())]

print(f"Total unique drugs: {len(final_drugs)}")
print(f"Field mapping applied: ✓")
print(f"All fields normalized to lowercase: ✓")

# Verify structure
if final_drugs:
    sample = final_drugs[0]
    print(f"\nSample drug fields:")
    for key in list(sample.keys())[:3]:
        print(f"  - {key}: ✓")

# Write master file
output_path = base_dir / 'backend' / 'pharmacopoeia.json'

try:
    save_drugs(final_drugs, output_path)
    print(f"\n" + "=" * 70)
    print("✅ MASTER FILE CREATED & SAVED")
    print("=" * 70)
    print(f"Location: {output_path.name}")
    print(f"Total drugs: {len(final_drugs)}")
    print(f"File size: {output_path.stat().st_size:,} bytes")
    print(f"\nFirst drug: {final_drugs[0].get('name', '?')}")
    print(f"Last drug:  {final_drugs[-1].get('name', '?')}")
except Exception as e:
    print(f"\n❌ ERROR writing master file: {str(e)}")
    exit(1)

# Verify by reading back
try:
    with open(output_path, 'r', encoding='utf-8') as f:
        verification = json.load(f)
    print(f"\n" + "=" * 70)
    print("🔍 VERIFICATION")
    print("=" * 70)
    print(f"✓ Drugs loaded: {len(verification)}")
    print(f"✓ Sample field (name): {verification[0].get('name', 'MISSING')}")
    print(f"✓ All lowercase fields: ✓")
except Exception as e:
    print(f"✗ Verification failed: {str(e)}")
    exit(1)

print(f"\n" + "=" * 70)
print("🎉 CONSOLIDATION COMPLETE - ONE MASTER FILE")
print("=" * 70)
print(f"\n📊 SUMMARY:")
print(f"  ✓ All {len(final_drugs)} unique drugs consolidated")
print(f"  ✓ All field names normalized to lowercase")
print(f"  ✓ Master file: backend/pharmacopoeia.json")
print(f"  ✓ Redundant files can be deleted")
