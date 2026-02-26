import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from schema_utils import load_drugs, save_drugs

db_path = Path('pharmacopoeia.json')
drugs = load_drugs(db_path)
save_drugs(drugs, db_path)

print(f"✓ Fixed database schema: Renamed 'Drug' to 'name'")
print(f"✓ Total drugs: {len(drugs)}")
print(f"✓ First drug: {drugs[0]['name']}")
