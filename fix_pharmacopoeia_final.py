#!/usr/bin/env python3
"""
FINAL FIX - Standardize field names in pharmacopoeia.json

This script delegates all field normalization and standardization to the shared backend/schema_utils.py module.
It ensures all field names are lowercase and required fields are present by orchestrating the process via schema_utils utilities.
Ensures valid JSON output.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'backend'))
from backend import schema_utils

file_path = Path('backend') / 'pharmacopoeia.json'

# Load, normalize, and save drugs using shared utilities
drugs = schema_utils.load_drugs(file_path)
schema_utils.save_drugs(drugs, file_path)

# Verify
schema_utils.verify_drugs_file(file_path)
print("\n✅ FIXED! All field normalization and standardization performed via schema_utils.\n")
