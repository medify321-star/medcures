"""
schema_utils.py - Shared utilities for pharmacopoeia database normalization and I/O
"""
import json
from pathlib import Path

# Field name mapping (all variations to canonical lowercase)
FIELD_MAPPING = {
    'drug': 'name',
    'Drug': 'name',
    'name': 'name',
    'category': 'category',
    'Category': 'category',
    'route': 'route',
    'Route': 'route',
    'storage': 'storage',
    'Storage': 'storage',
    'dose': 'dose',
    'Dose': 'dose',
    'uses': 'uses',
    'Uses': 'uses',
    'side_effects': 'side_effects',
    'Side Effects': 'side_effects',
    'side_effect': 'side_effects',
    'side_effects_in_arabic': 'side_effects',
    'citations': 'citations',
    'citation': 'citations',
    'Citation': 'citations',
    'disclaimer': 'disclaimer',
    'Disclaimer': 'disclaimer',
}

REQUIRED_FIELDS = [
    'name', 'category', 'route', 'storage', 'dose',
    'uses', 'side_effects', 'citations', 'disclaimer'
]

def normalize_drug_fields(drug):
    """Return a new dict with normalized field names and all required fields."""
    norm = {}
    for k, v in drug.items():
        key = FIELD_MAPPING.get(k, k).lower()
        norm[key] = v
    # Ensure all required fields exist
    for field in REQUIRED_FIELDS:
        if field not in norm:
            norm[field] = ""
    # Only keep required fields, in order
    return {field: norm[field] for field in REQUIRED_FIELDS}

def load_drugs(path):
    """Load and normalize all drugs from a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [normalize_drug_fields(d) for d in data]

def save_drugs(drugs, path):
    """Save normalized drugs to a JSON file."""
    # Sort by name for consistency
    drugs_sorted = sorted(drugs, key=lambda x: x.get('name', '').lower())
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(drugs_sorted, f, indent=2, ensure_ascii=False)

def verify_drugs_file(path):
    """Quick verification: loads file, prints summary."""
    drugs = load_drugs(path)
    print(f"✓ {len(drugs)} drugs loaded from {path}")
    if drugs:
        print(f"  First: {drugs[0]['name']}")
        print(f"  Last:  {drugs[-1]['name']}")
        print(f"  Fields: {list(drugs[0].keys())}")
    else:
        print("  No drugs found.")