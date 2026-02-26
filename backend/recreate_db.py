import json

# Original drug data provided by user (first batch)
drugs_data = """
Drug common name: Paracetamol (Acetaminophen)
Category: Analgesic, Antipyretic
Route: Oral, Rectal, IV
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 500-1000 mg every 4-6 hours (max 4 g/day)
Uses: Mild-moderate pain, Fever reduction, Headache
Side effects: Nausea, Rash, Liver toxicity (overdose)
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Ibuprofen
Category: Analgesic, NSAID
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 200-400 mg every 6-8 hours (max 1200 mg/day OTC)
Uses: Pain relief, Inflammation, Fever
Side effects: GI upset, Headache, Dizziness
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Morphine
Category: Analgesic (Opioid)
Route: Oral, IV, IM, Subcutaneous
Storage: Below 25°C, protect from light
Typical dose: Adults: 10-30 mg every 4 hours
Uses: Severe pain, Post-surgical pain, Cancer pain
Side effects: Constipation, Nausea, Respiratory depression
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Aspirin
Category: Analgesic, Antiplatelet
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 75-325 mg once daily
Uses: Pain relief, Fever, Cardiovascular protection
Side effects: GI bleeding, Nausea, Tinnitus
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Amoxicillin
Category: Antibiotic (Beta-lactam, Penicillin)
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 500 mg every 8 hours
Uses: Respiratory infections, Urinary tract infections, Skin infections
Side effects: Diarrhea, Rash, Nausea
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Azithromycin
Category: Antibiotic (Macrolide)
Route: Oral, IV
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 500 mg once daily for 3 days
Uses: Respiratory infections, Skin infections, STDs
Side effects: Diarrhea, Nausea, Abdominal pain
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Ciprofloxacin
Category: Antibiotic (Fluoroquinolone)
Route: Oral, IV
Storage: Below 25°C, protect from light
Typical dose: Adults: 500 mg every 12 hours
Uses: UTIs, Respiratory infections, GI infections
Side effects: Nausea, Dizziness, Tendon rupture (rare)
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Doxycycline
Category: Antibiotic (Tetracycline)
Route: Oral, IV
Storage: Below 25°C, protect from light
Typical dose: Adults: 100 mg every 12 hours
Uses: Respiratory infections, Malaria prophylaxis, Acne
Side effects: Photosensitivity, Nausea, Diarrhea
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Metformin
Category: Antidiabetic (Biguanide)
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 500-1000 mg twice daily (max 2 g/day)
Uses: Type 2 diabetes, Insulin resistance, PCOS (off-label)
Side effects: GI upset, Metallic taste, Lactic acidosis (rare)
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Insulin
Category: Antidiabetic (Hormone)
Route: Subcutaneous, IV, IM
Storage: 2-8°C, protect from light
Typical dose: Varies (individualized dosing)
Uses: Type 1 diabetes, Type 2 diabetes (advanced), Gestational diabetes
Side effects: Hypoglycemia, Weight gain, Lipodystrophy
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Atorvastatin
Category: Statin (Lipid-lowering)
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 20-80 mg once daily
Uses: High cholesterol, Cardiovascular disease prevention
Side effects: Muscle pain, Elevated liver enzymes, Nausea
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Lisinopril
Category: ACE inhibitor (Antihypertensive)
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 10-40 mg once daily
Uses: Hypertension, Heart failure, Post-MI
Side effects: Cough, Dizziness, Hyperkalemia
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Amlodipine
Category: Calcium channel blocker (Antihypertensive)
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 5-10 mg once daily
Uses: Hypertension, Angina
Side effects: Headache, Flushing, Ankle edema
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Omeprazole
Category: Proton pump inhibitor
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 20-40 mg once daily
Uses: GERD, Peptic ulcer disease, Gastritis
Side effects: Headache, Diarrhea, Nausea
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Cetirizine
Category: Antihistamine
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 10 mg once daily
Uses: Allergies, Urticaria, Itching
Side effects: Drowsiness, Dry mouth, Headache
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Salbutamol
Category: Beta-2 agonist (Bronchodilator)
Route: Oral, Inhalation
Storage: Below 25°C, protect from light
Typical dose: 2 puffs every 4-6 hours as needed
Uses: Asthma, COPD, Acute bronchospasm
Side effects: Tremor, Tachycardia, Nervousness
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Fluticasone
Category: Corticosteroid (Inhaled)
Route: Inhalation, Nasal
Storage: Below 25°C, protect from moisture
Typical dose: 88-220 mcg twice daily
Uses: Asthma control, Seasonal allergies, Rhinitis
Side effects: Oral thrush, Hoarseness, Cough
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Famotidine
Category: H2-receptor antagonist
Route: Oral, IV
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 20 mg twice daily or 40 mg at bedtime
Uses: GERD, Peptic ulcer disease, Gastritis
Side effects: Headache, Diarrhea, Constipation
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Simvastatin
Category: Statin (Lipid-lowering)
Route: Oral
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 20-80 mg once daily at night
Uses: High cholesterol, Cardiovascular disease prevention
Side effects: Muscle pain, Elevated liver enzymes, Nausea
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.

Drug common name: Diclofenac
Category: NSAID
Route: Oral, Injection, Topical
Storage: Below 25°C, protect from moisture
Typical dose: Adults: 75-150 mg daily in divided doses
Uses: Pain relief, Inflammation, Fever
Side effects: GI upset, Dizziness, Rash
Citation: WHO Essential Medicines List
Disclaimer: Educational use only. Consult a physician for medical advice.
"""

def parse_drugs(text):
    drugs = []
    blocks = text.split("Drug common name:")[1:]
    
    for block in blocks:
        lines = block.strip().split("\n")
        drug_data = {}
        
        for line in lines:
            if not line.strip():
                continue
            if ":" not in line:
                continue
                
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            # Map to correct field names
            if key == "Drug common name":
                drug_data["name"] = value
            elif key == "Category":
                drug_data["category"] = value
            elif key == "Route":
                drug_data["route"] = value
            elif key == "Storage":
                drug_data["storage"] = value
            elif key == "Typical dose":
                drug_data["dose"] = value
            elif key == "Uses":
                drug_data["uses"] = [u.strip() for u in value.split(",")]
            elif key == "Side effects":
                drug_data["side_effects"] = [s.strip() for s in value.split(",")]
            elif key == "Citation":
                drug_data["citations"] = [value]
            elif key == "Disclaimer":
                drug_data["disclaimer"] = value
        
        if "name" in drug_data:
            drugs.append(drug_data)
    
    return drugs

# Parse the drugs
parsed_drugs = parse_drugs(drugs_data)

# Save to file
with open("pharmacopoeia.json", "w", encoding="utf-8") as f:
    json.dump(parsed_drugs, f, indent=2, ensure_ascii=False)

print(f"✓ Database recreated!")
print(f"✓ Total drugs: {len(parsed_drugs)}")
print(f"✓ First drug: {parsed_drugs[0]['name']}")
print(f"✓ Last drug: {parsed_drugs[-1]['name']}")
