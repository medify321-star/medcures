# Pharmacopoeia Database Structure

## Current Database: `pharmacopoeia.json`

**Format:** JSON Array of Drug Objects

### Drug Object Structure

```json
{
  "name": "Drug Name",
  "category": "Drug Category / Classification",
  "route": "Route of Administration",
  "storage": "Storage Instructions",
  "dose": "Dosage Information",
  "uses": "Medical Uses",
  "side_effects": "Potential Side Effects",
  "citations": ["Citation 1", "Citation 2"]
}
```

## Current Drugs (5 Total)

### 1. Aspirin
- **Category:** Analgesic / Antiplatelet
- **Route:** Oral
- **Dosage:** 75-325 mg daily (antiplatelet); 300-600 mg every 4-6 hours (analgesic)
- **Uses:** Pain relief, fever reduction, prevention of blood clots
- **Side Effects:** GI irritation, bleeding risk, allergic reactions

### 2. Paracetamol
- **Category:** Analgesic / Antipyretic
- **Route:** Oral, Rectal, Intravenous
- **Dosage:** 500-1000 mg every 4-6 hours (max 4 g/day)
- **Uses:** Pain relief, fever reduction
- **Side Effects:** Liver toxicity in overdose, rare allergic reactions

### 3. Amoxicillin
- **Category:** Antibiotic (Penicillin class)
- **Route:** Oral
- **Dosage:** 250-500 mg every 8 hours
- **Uses:** Treatment of bacterial infections
- **Side Effects:** Diarrhea, nausea, rash, allergic reactions

### 4. Ibuprofen
- **Category:** NSAID (Non-steroidal anti-inflammatory)
- **Route:** Oral
- **Dosage:** 200-400 mg every 4-6 hours (max 1200 mg/day OTC)
- **Uses:** Pain relief, inflammation reduction, fever reduction
- **Side Effects:** GI irritation, kidney effects, bleeding risk

### 5. Metformin
- **Category:** Antidiabetic (Biguanide)
- **Route:** Oral
- **Dosage:** 500-850 mg twice to three times daily (max 2 g/day)
- **Uses:** Type 2 diabetes management, improve insulin sensitivity
- **Side Effects:** GI upset, vitamin B12 deficiency with long-term use

## How to Add New Drugs

1. Edit `backend/pharmacopoeia.json`
2. Add new drug object to the JSON array
3. Ensure all fields are filled:
   - name
   - category
   - route
   - storage
   - dose
   - uses
   - side_effects
   - citations (array of strings)
4. Backend auto-reloads (with --reload flag)
5. Test via chat interface

## Example: Adding a New Drug

```json
{
  "name": "Lisinopril",
  "category": "ACE Inhibitor / Antihypertensive",
  "route": "Oral",
  "storage": "Store at room temperature",
  "dose": "10-40 mg once daily",
  "uses": "Management of hypertension and heart failure",
  "side_effects": "Dry cough, dizziness, hyperkalemia",
  "citations": ["BP 2024", "USP", "FDA"]
}
```

## Backend Integration

- Backend loads pharmacopoeia.json on startup
- Frontend searches drugs via API endpoint
- Chat responses include drug information
- Fallback formatting if API unavailable

## File Location
```
c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent\backend\pharmacopoeia.json
```

## Last Updated
February 22, 2026
