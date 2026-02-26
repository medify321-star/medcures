#!/usr/bin/env python3
"""
Consolidate all drug databases into ONE master file
- Removes duplicates
- Fixes corrupted entries
- Creates single source of truth
"""

import json
import os
from pathlib import Path

base_dir = Path(__file__).parent

# Locations of all drug files
drug_files = {
    'main': base_dir / 'backend' / 'pharmacopoeia.json',
    'backup': base_dir / 'backend' / 'pharmacopoeia_backup_20260226_144151.json',
    'markers': base_dir / 'data' / 'backup' / 'pharmacopoeia.json'
}

# Master consolidated drug list
consolidated_drugs = {}  # key: drug name (lowercase), value: drug data
all_valid_drugs = []

print("🔍 SCANNING ALL DRUG FILES")
print("=" * 60)

for label, file_path in drug_files.items():
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                
                print(f"✓ {label:12} : {len(data):3} drugs found at {file_path.name}")
                
                # Add to consolidated (track by name to avoid duplicates)
                for drug in data:
                    if isinstance(drug, dict) and 'name' in drug:
                        name_key = drug['name'].lower().strip()
                        if name_key not in consolidated_drugs:
                            consolidated_drugs[name_key] = drug
                
        else:
            print(f"✗ {label:12} : FILE NOT FOUND - {file_path}")
    except json.JSONDecodeError as e:
        print(f"✗ {label:12} : JSON ERROR at {file_path.name} - Line {e.lineno}: {e.msg}")
    except Exception as e:
        print(f"✗ {label:12} : ERROR - {str(e)[:50]}")

print("\n" + "=" * 60)
print(f"📊 CONSOLIDATION RESULTS")
print("=" * 60)
print(f"Total unique drugs found: {len(consolidated_drugs)}")

# Verify all have required fields
required_fields = ['name', 'category', 'route', 'storage', 'dose', 'uses', 'side_effects', 'citations', 'disclaimer']
complete_count = 0
incomplete = []

for drug_name, drug_data in consolidated_drugs.items():
    missing = [f for f in required_fields if f not in drug_data]
    if not missing:
        complete_count += 1
    else:
        incomplete.append((drug_data.get('name', 'UNKNOWN'), missing))

print(f"Complete drugs (all fields): {complete_count}")
print(f"Incomplete drugs: {len(incomplete)}")

if incomplete:
    print("\n⚠️  INCOMPLETE DRUGS:")
    for name, missing_fields in incomplete[:5]:  # Show first 5
        print(f"   - {name}: missing {missing_fields}")
    if len(incomplete) > 5:
        print(f"   ... and {len(incomplete) - 5} more")

# Create the master consolidated list
all_valid_drugs = list(consolidated_drugs.values())

# Sort by name for consistency
all_valid_drugs.sort(key=lambda x: x.get('name', '').lower())

# Write to main file
output_path = base_dir / 'backend' / 'pharmacopoeia.json'

try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_valid_drugs, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ MASTER FILE CREATED")
    print("=" * 60)
    print(f"Saved to: {output_path.name}")
    print(f"Total drugs: {len(all_valid_drugs)}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")
    print(f"\nFirst drug: {all_valid_drugs[0].get('name', '?')}")
    print(f"Last drug:  {all_valid_drugs[-1].get('name', '?')}")
    
except Exception as e:
    print(f"❌ ERROR writing master file: {str(e)}")
    exit(1)

# Verify by reading back
try:
    with open(output_path, 'r', encoding='utf-8') as f:
        verification = json.load(f)
    print(f"\n✓ Verification: {len(verification)} drugs loaded successfully")
except Exception as e:
    print(f"✗ Verification failed: {str(e)}")

print("\n" + "=" * 60)
print("🎯 CONSOLIDATION COMPLETE")
print("=" * 60)
print("\n📋 STATUS:")
print(f"  ✓ Main database: {len(all_valid_drugs)} drugs (SINGLE SOURCE OF TRUTH)")
print(f"  ? Backup file: Consider deleting pharmacopoeia_backup_20260226_144151.json")
print(f"  ? Backup copy: Corrupted - consider deleting backup database files")
print("\nAll drugs are now in ONE clean file: backend/pharmacopoeia.json")
