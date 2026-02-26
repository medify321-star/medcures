#!/usr/bin/env python3
"""
Script to parse and import drug data into pharmacopoeia.json
"""

import json
import re

# User-provided drug data (raw text)
raw_drugs_text = """
Drug common name: Paracetamol (Acetaminophen)
Category: Analgesic, Antipyretic
Route: Oral, Rectal, Intravenous
Storage: Store below 25°C, protect from moisture
Typical dose: Adults 500–1000 mg every 4–6 hours (max 4 g/day) [general reference only]
Uses: Pain relief, fever reduction
Side effects: Nausea, rash, liver damage in overdose
Citation: WHO Model List of Essential Medicines, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ibuprofen
Category: NSAID (Non‑steroidal anti‑inflammatory drug)
Route: Oral
Storage: Store below 25°C, protect from moisture
Typical dose: Adults 200–400 mg every 6–8 hours [general reference only]
Uses: Pain relief, inflammation reduction, fever
Side effects: Stomach upset, ulcers, kidney issues
Citation: WHO Model List of Essential Medicines, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Amoxicillin
Category: Antibiotic (Penicillin class)
Route: Oral
Storage: Store at room temperature, protect from moisture
Typical dose: Adults 500 mg every 8 hours [general reference only]
Uses: Bacterial infections (respiratory, urinary, skin)
Side effects: Diarrhea, rash, allergic reactions
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Cetirizine
Category: Antihistamine
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10 mg once daily [general reference only]
Uses: Allergy relief (hay fever, hives)
Side effects: Drowsiness, dry mouth
Citation: FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Metformin
Category: Antidiabetic (Biguanide)
Route: Oral
Storage: Store below 30°C
Typical dose: Adults 500–2000 mg daily in divided doses [general reference only]
Uses: Type 2 diabetes management
Side effects: Nausea, diarrhea, rare lactic acidosis
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Aspirin
Category: NSAID, Antiplatelet
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 75–325 mg daily (cardiovascular use) [general reference only]
Uses: Pain relief, fever reduction, blood thinning
Side effects: Stomach irritation, bleeding risk
Citation: WHO Model List of Essential Medicines, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Omeprazole
Category: Proton Pump Inhibitor (PPI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 20–40 mg once daily [general reference only]
Uses: Acid reflux, stomach ulcers
Side effects: Headache, diarrhea, long‑term vitamin deficiency
Citation: FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Salbutamol (Albuterol)
Category: Beta‑2 agonist (Bronchodilator)
Route: Inhalation, Oral
Storage: Store below 25°C
Typical dose: Inhalation 100–200 mcg every 4–6 hours [general reference only]
Uses: Asthma, bronchospasm relief
Side effects: Tremors, rapid heartbeat
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Loratadine
Category: Antihistamine (non‑sedating)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10 mg once daily [general reference only]
Uses: Allergy relief
Side effects: Headache, dry mouth
Citation: FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Doxycycline
Category: Antibiotic (Tetracycline class)
Route: Oral
Storage: Store below 25°C, protect from light
Typical dose: Adults 100 mg once or twice daily [general reference only]
Uses: Infections, acne, malaria prevention
Side effects: Sun sensitivity, stomach upset
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Atorvastatin
Category: Statin (Lipid‑lowering agent)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10–80 mg once daily [general reference only]
Uses: High cholesterol, cardiovascular risk reduction
Side effects: Muscle pain, liver enzyme elevation
Citation: FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Furosemide
Category: Loop diuretic
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 20–80 mg once or twice daily [general reference only]
Uses: Edema, hypertension
Side effects: Dehydration, electrolyte imbalance
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Prednisolone
Category: Corticosteroid
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 5–60 mg daily depending on condition [general reference only]
Uses: Inflammation, autoimmune disorders
Side effects: Weight gain, mood changes, osteoporosis
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Diazepam
Category: Benzodiazepine
Route: Oral, Intravenous, Rectal
Storage: Store below 25°C
Typical dose: Adults 2–10 mg 2–4 times daily [general reference only]
Uses: Anxiety, seizures, muscle spasms
Side effects: Drowsiness, dependence risk
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Insulin (Human)
Category: Hormone (Antidiabetic)
Route: Subcutaneous, Intravenous
Storage: Refrigerate at 2–8°C
Typical dose: Individualized, varies widely [general reference only]
Uses: Diabetes mellitus
Side effects: Hypoglycemia, weight gain
Citation: WHO Model List of Essential Medicines, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Morphine
Category: Opioid analgesic
Route: Oral, Intravenous, Subcutaneous
Storage: Store below 25°C
Typical dose: Adults 10–30 mg every 4 hours (oral) [general reference only]
Uses: Severe pain management
Side effects: Constipation, drowsiness, dependence risk
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Chlorpheniramine
Category: Antihistamine
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 4 mg every 4–6 hours [general reference only]
Uses: Allergy relief
Side effects: Drowsiness, dry mouth
Citation: FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ranitidine (Note: withdrawn in many countries)
Category: H2 receptor antagonist
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 150 mg twice daily [general reference only]
Uses: Acid reflux, ulcers
Side effects: Headache, diarrhea
Citation: FDA Drug Database (historical)
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hydrocortisone
Category: Corticosteroid
Route: Oral, Topical, Intravenous
Storage: Store below 25°C
Typical dose: Adults 20–240 mg daily depending on condition [general reference only]
Uses: Inflammation, adrenal insufficiency
Side effects: Immunosuppression, weight gain
Citation: WHO Model List of Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Levothyroxine
Category: Thyroid hormone replacement
Route: Oral
Storage: Store below 25°C, protect from light
Typical dose: Adults 25–200 mcg daily [general reference only]
Uses: Hypothyroidism, thyroid hormone deficiency
Side effects: Palpitations, insomnia, weight loss
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Rosuvastatin
Category: Statin (lipid-lowering agent)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–40 mg once daily [general reference only]
Uses: High cholesterol, cardiovascular risk reduction
Side effects: Muscle pain, liver enzyme elevation
Citation: FDA Drug Database, WHO Essential Medicines
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Esomeprazole
Category: Proton Pump Inhibitor (PPI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 20–40 mg once daily [general reference only]
Uses: GERD, heartburn, peptic ulcers
Side effects: Headache, diarrhea, vitamin B12 deficiency (long-term)
Citation: DailyMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Valsartan
Category: Angiotensin II receptor blocker (ARB)
Route: Oral
Storage: Store below 30°C
Typical dose: Adults 80–320 mg once daily [general reference only]
Uses: Hypertension, heart failure
Side effects: Dizziness, kidney impairment, hyperkalemia
Citation: WHO Essential Medicines, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Duloxetine
Category: SNRI (Serotonin-Norepinephrine Reuptake Inhibitor)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 30–120 mg daily [general reference only]
Uses: Depression, anxiety, neuropathic pain
Side effects: Nausea, dry mouth, insomnia
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Lisdexamfetamine
Category: CNS stimulant
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 30–70 mg once daily [general reference only]
Uses: ADHD, binge eating disorder
Side effects: Insomnia, decreased appetite, increased heart rate
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Pregabalin
Category: Anticonvulsant, neuropathic pain agent
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 150–600 mg daily in divided doses [general reference only]
Uses: Neuropathic pain, partial seizures, fibromyalgia
Side effects: Dizziness, weight gain, blurred vision
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tiotropium bromide
Category: Anticholinergic (bronchodilator)
Route: Inhalation
Storage: Store below 25°C
Typical dose: Adults 18 mcg once daily (inhalation) [general reference only]
Uses: COPD, asthma maintenance
Side effects: Dry mouth, constipation, urinary retention
Citation: WHO Essential Medicines, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Gabapentin
Category: Anticonvulsant, neuropathic pain agent
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 900–3600 mg daily in divided doses [general reference only]
Uses: Neuropathic pain, seizures
Side effects: Drowsiness, dizziness, weight gain
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Clonazepam
Category: Benzodiazepine
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 0.5–2 mg two to three times daily [general reference only]
Uses: Seizure disorders, panic disorder
Side effects: Drowsiness, dependence risk, impaired coordination
Citation: WHO Essential Medicines, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Amlodipine
Category: Calcium channel blocker (antihypertensive)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–10 mg once daily [general reference only]
Uses: Hypertension, angina
Side effects: Swelling of ankles, dizziness, flushing
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Enalapril
Category: ACE inhibitor (antihypertensive)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–40 mg daily in divided doses [general reference only]
Uses: Hypertension, heart failure
Side effects: Dry cough, dizziness, kidney impairment
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Spironolactone
Category: Potassium-sparing diuretic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 25–100 mg daily [general reference only]
Uses: Heart failure, hypertension, edema
Side effects: Hyperkalemia, gynecomastia
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Rifampicin
Category: Antibiotic (antitubercular)
Route: Oral
Storage: Store below 25°C, protect from light
Typical dose: Adults 10 mg/kg once daily [general reference only]
Uses: Tuberculosis, leprosy
Side effects: Liver toxicity, red-orange urine discoloration
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Isoniazid
Category: Antibiotic (antitubercular)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5 mg/kg daily [general reference only]
Uses: Tuberculosis
Side effects: Peripheral neuropathy, liver toxicity
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Zidovudine
Category: Antiretroviral (NRTI)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 300 mg twice daily [general reference only]
Uses: HIV/AIDS treatment
Side effects: Anemia, headache, nausea
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Efavirenz
Category: Antiretroviral (NNRTI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 600 mg once daily [general reference only]
Uses: HIV/AIDS treatment
Side effects: Dizziness, vivid dreams, rash
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Artesunate
Category: Antimalarial
Route: Oral, Intravenous
Storage: Store below 25°C, protect from moisture
Typical dose: Adults 2–4 mg/kg daily [general reference only]
Uses: Severe malaria
Side effects: Dizziness, low white blood cell count
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Albendazole
Category: Anthelmintic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 400 mg once daily (varies by infection) [general reference only]
Uses: Parasitic worm infections
Side effects: Abdominal pain, headache, liver enzyme elevation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Methotrexate
Category: Antimetabolite (immunosuppressant, anticancer)
Route: Oral, Intravenous
Storage: Store below 25°C, protect from light
Typical dose: Adults 7.5–25 mg weekly (autoimmune use) [general reference only]
Uses: Rheumatoid arthritis, psoriasis, cancers
Side effects: Bone marrow suppression, liver toxicity, nausea
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hydrochlorothiazide
Category: Thiazide diuretic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 12.5–50 mg once daily [general reference only]
Uses: Hypertension, edema
Side effects: Low potassium, dizziness, increased urination
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Warfarin
Category: Anticoagulant (Vitamin K antagonist)
Route: Oral
Storage: Store below 25°C
Typical dose: Individualized based on INR monitoring [general reference only]
Uses: Prevention of blood clots, atrial fibrillation, DVT
Side effects: Bleeding, bruising, drug interactions
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Clopidogrel
Category: Antiplatelet agent
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 75 mg once daily [general reference only]
Uses: Prevention of stroke, heart attack
Side effects: Bleeding, rash, diarrhea
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Digoxin
Category: Cardiac glycoside
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 0.125–0.25 mg daily [general reference only]
Uses: Heart failure, atrial fibrillation
Side effects: Nausea, vision changes, arrhythmias
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Levofloxacin
Category: Fluoroquinolone antibiotic
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 500–750 mg once daily [general reference only]
Uses: Respiratory infections, urinary tract infections
Side effects: Tendon rupture, dizziness, nausea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Linezolid
Category: Oxazolidinone antibiotic
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 600 mg every 12 hours [general reference only]
Uses: Resistant bacterial infections (MRSA, VRE)
Side effects: Bone marrow suppression, headache
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Fluconazole
Category: Antifungal (azole class)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 150–400 mg daily depending on infection [general reference only]
Uses: Fungal infections (candidiasis, cryptococcosis)
Side effects: Nausea, liver enzyme elevation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tamoxifen
Category: Selective estrogen receptor modulator (SERM)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 20 mg once daily [general reference only]
Uses: Breast cancer treatment and prevention
Side effects: Hot flashes, risk of blood clots
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Allopurinol
Category: Xanthine oxidase inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100–300 mg daily [general reference only]
Uses: Gout, hyperuricemia
Side effects: Rash, liver enzyme elevation
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Haloperidol
Category: Antipsychotic (typical)
Route: Oral, Intramuscular
Storage: Store below 25°C
Typical dose: Adults 2–20 mg daily [general reference only]
Uses: Schizophrenia, acute psychosis
Side effects: Extrapyramidal symptoms, sedation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Topiramate
Category: Anticonvulsant
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100–400 mg daily in divided doses [general reference only]
Uses: Epilepsy, migraine prevention
Side effects: Cognitive slowing, weight loss, tingling sensations
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Lamotrigine
Category: Anticonvulsant, mood stabilizer
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100–400 mg daily [general reference only]
Uses: Epilepsy, bipolar disorder
Side effects: Rash (rare severe), dizziness, headache
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Sertraline
Category: SSRI (Selective Serotonin Reuptake Inhibitor)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 50–200 mg daily [general reference only]
Uses: Depression, anxiety disorders
Side effects: Nausea, insomnia, sexual dysfunction
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Venlafaxine
Category: SNRI (Serotonin-Norepinephrine Reuptake Inhibitor)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 75–225 mg daily [general reference only]
Uses: Depression, anxiety, panic disorder
Side effects: Sweating, nausea, hypertension
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Quetiapine
Category: Atypical antipsychotic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 150–800 mg daily [general reference only]
Uses: Schizophrenia, bipolar disorder, depression adjunct
Side effects: Sedation, weight gain, metabolic changes
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Risperidone
Category: Atypical antipsychotic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 2–8 mg daily [general reference only]
Uses: Schizophrenia, bipolar disorder, irritability in autism
Side effects: Weight gain, tremors, drowsiness
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Lithium carbonate
Category: Mood stabilizer
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 600–1200 mg daily (dose adjusted by blood levels) [general reference only]
Uses: Bipolar disorder
Side effects: Tremors, thyroid dysfunction, kidney effects
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Buspirone
Category: Anxiolytic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 15–60 mg daily in divided doses [general reference only]
Uses: Generalized anxiety disorder
Side effects: Dizziness, headache, nausea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Bupropion
Category: Antidepressant (NDRI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 150–450 mg daily [general reference only]
Uses: Depression, smoking cessation
Side effects: Insomnia, dry mouth, seizure risk at high doses
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Aripiprazole
Category: Atypical antipsychotic
Route: Oral, Intramuscular
Storage: Store below 25°C
Typical dose: Adults 10–30 mg daily [general reference only]
Uses: Schizophrenia, bipolar disorder, depression adjunct
Side effects: Akathisia, weight gain, insomnia
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Glimepiride
Category: Sulfonylurea (antidiabetic)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 1–8 mg once daily [general reference only]
Uses: Type 2 diabetes
Side effects: Hypoglycemia, weight gain
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Sitagliptin
Category: DPP-4 inhibitor (antidiabetic)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100 mg once daily [general reference only]
Uses: Type 2 diabetes
Side effects: Headache, pancreatitis (rare)
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Empagliflozin
Category: SGLT2 inhibitor (antidiabetic)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10–25 mg once daily [general reference only]
Uses: Type 2 diabetes, heart failure
Side effects: Urinary tract infections, dehydration
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Glibenclamide (Glyburide)
Category: Sulfonylurea (antidiabetic)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 2.5–20 mg daily [general reference only]
Uses: Type 2 diabetes
Side effects: Hypoglycemia, weight gain
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Nifedipine
Category: Calcium channel blocker
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10–60 mg daily [general reference only]
Uses: Hypertension, angina
Side effects: Flushing, headache, ankle swelling
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Verapamil
Category: Calcium channel blocker
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 120–480 mg daily [general reference only]
Uses: Hypertension, arrhythmias, angina
Side effects: Constipation, dizziness, low blood pressure
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Diltiazem
Category: Calcium channel blocker
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 120–360 mg daily [general reference only]
Uses: Hypertension, angina, arrhythmias
Side effects: Edema, headache, bradycardia
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Propranolol
Category: Beta-blocker
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 40–320 mg daily [general reference only]
Uses: Hypertension, arrhythmias, migraine prevention
Side effects: Fatigue, bradycardia, depression
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Atenolol
Category: Beta-blocker
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 25–100 mg daily [general reference only]
Uses: Hypertension, angina
Side effects: Fatigue, dizziness, cold extremities
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Metoprolol
Category: Beta-blocker
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 50–200 mg daily [general reference only]
Uses: Hypertension, heart failure, arrhythmias
Side effects: Fatigue, bradycardia, dizziness
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Carvedilol
Category: Beta-blocker (non-selective with alpha-blocking activity)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 6.25–50 mg daily [general reference only]
Uses: Heart failure, hypertension
Side effects: Dizziness, fatigue, low blood pressure
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hydralazine
Category: Vasodilator
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 25–100 mg daily [general reference only]
Uses: Hypertension, heart failure
Side effects: Headache, palpitations, lupus-like syndrome
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Isosorbide mononitrate
Category: Nitrate (vasodilator)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 20–60 mg daily [general reference only]
Uses: Angina prevention
Side effects: Headache, dizziness, flushing
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Nitroglycerin
Category: Nitrate (vasodilator)
Route: Sublingual, Transdermal, Intravenous
Storage: Store below 25°C, protect from light
Typical dose: Sublingual 0.3–0.6 mg as needed [general reference only]
Uses: Angina relief
Side effects: Headache, dizziness, flushing
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Heparin
Category: Anticoagulant
Route: Intravenous, Subcutaneous
Storage: Store below 25°C
Typical dose: Individualized based on clotting tests [general reference only]
Uses: Prevention and treatment of blood clots
Side effects: Bleeding, thrombocytopenia
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Enoxaparin
Category: Low molecular weight heparin (anticoagulant)
Route: Subcutaneous
Storage: Store below 25°C
Typical dose: Adults 40 mg once daily (prophylaxis) [general reference only]
Uses: Prevention of DVT, treatment of clots
Side effects: Bleeding, injection site reactions
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Dabigatran
Category: Direct thrombin inhibitor (anticoagulant)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 150 mg twice daily [general reference only]
Uses: Prevention of stroke in atrial fibrillation, DVT
Side effects: Bleeding, stomach upset
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Rivaroxaban
Category: Factor Xa inhibitor (anticoagulant)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10–20 mg once daily [general reference only]
Uses: Prevention of stroke, treatment of DVT
Side effects: Bleeding, anemia
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Apixaban
Category: Factor Xa inhibitor (anticoagulant)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5 mg twice daily [general reference only]
Uses: Prevention of stroke, treatment of DVT
Side effects: Bleeding, nausea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Aciclovir
Category: Antiviral
Route: Oral, Intravenous, Topical
Storage: Store below 25°C
Typical dose: Adults 200–800 mg 5 times daily [general reference only]
Uses: Herpes simplex, varicella-zoster
Side effects: Nausea, headache, kidney effects
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Oseltamivir
Category: Antiviral (neuraminidase inhibitor)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 75 mg twice daily [general reference only]
Uses: Influenza treatment and prevention
Side effects: Nausea, vomiting, headache
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Remdesivir
Category: Antiviral
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 200 mg day 1, then 100 mg daily [general reference only]
Uses: COVID-19 treatment
Side effects: Nausea, liver enzyme elevation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Favipiravir
Category: Antiviral
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 1600 mg twice daily day 1, then 600 mg twice daily [general reference only]
Uses: Influenza, COVID-19 (investigational)
Side effects: Elevated uric acid, gastrointestinal upset
Citation: PubMed, WHO Essential Medicines List
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Sofosbuvir
Category: Antiviral (HCV polymerase inhibitor)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 400 mg once daily [general reference only]
Uses: Hepatitis C treatment
Side effects: Fatigue, headache, nausea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tenofovir disoproxil fumarate
Category: Antiretroviral (NRTI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 300 mg once daily [general reference only]
Uses: HIV/AIDS, Hepatitis B
Side effects: Kidney toxicity, bone loss
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Lamivudine
Category: Antiretroviral (NRTI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 150 mg twice daily [general reference only]
Uses: HIV/AIDS, Hepatitis B
Side effects: Headache, fatigue, nausea
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Nevirapine
Category: Antiretroviral (NNRTI)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 200 mg twice daily [general reference only]
Uses: HIV/AIDS treatment
Side effects: Rash, liver toxicity
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Lopinavir/Ritonavir
Category: Antiretroviral (protease inhibitor combination)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 400/100 mg twice daily [general reference only]
Uses: HIV/AIDS treatment
Side effects: Diarrhea, nausea, lipid changes
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Dolutegravir
Category: Antiretroviral (integrase inhibitor)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 50 mg once daily [general reference only]
Uses: HIV/AIDS treatment
Side effects: Insomnia, headache, weight gain
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hydroxychloroquine
Category: Antimalarial, immunomodulator
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 200–400 mg daily [general reference only]
Uses: Malaria, lupus, rheumatoid arthritis
Side effects: Retinal toxicity, nausea
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Chloroquine
Category: Antimalarial
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 300 mg once weekly (prophylaxis) [general reference only]
Uses: Malaria treatment and prevention
Side effects: Itching, retinal toxicity
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Mefloquine
Category: Antimalarial
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 250 mg once weekly (prophylaxis) [general reference only]
Uses: Malaria prevention
Side effects: Vivid dreams, dizziness, psychiatric effects
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Primaquine
Category: Antimalarial
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 15 mg daily for 14 days [general reference only]
Uses: Malaria (eradication of hypnozoites)
Side effects: Hemolysis in G6PD deficiency, nausea
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Clindamycin
Category: Antibiotic (lincosamide)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 150–450 mg every 6 hours [general reference only]
Uses: Skin infections, anaerobic infections
Side effects: Diarrhea, C. difficile colitis
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Azithromycin
Category: Antibiotic (macrolide)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 500 mg day 1, then 250 mg daily [general reference only]
Uses: Respiratory infections, STDs
Side effects: Diarrhea, nausea, QT prolongation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Clarithromycin
Category: Antibiotic (macrolide)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 250–500 mg twice daily [general reference only]
Uses: Respiratory infections, H. pylori
Side effects: Nausea, diarrhea, taste changes
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Erythromycin
Category: Antibiotic (macrolide)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 250–500 mg every 6 hours [general reference only]
Uses: Respiratory infections, skin infections
Side effects: Nausea, diarrhea, QT prolongation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vancomycin
Category: Antibiotic (glycopeptide)
Route: Intravenous, Oral (for C. difficile)
Storage: Store below 25°C
Typical dose: Adults 500–1000 mg every 12 hours [general reference only]
Uses: MRSA infections, C. difficile colitis
Side effects: Red man syndrome, kidney toxicity
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Amphotericin B
Category: Antifungal
Route: Intravenous
Storage: Refrigerate, protect from light
Typical dose: Adults 0.25–1 mg/kg daily [general reference only]
Uses: Severe fungal infections
Side effects: Kidney toxicity, fever, chills
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Itraconazole
Category: Antifungal (azole class)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100–200 mg daily [general reference only]
Uses: Fungal infections (aspergillosis, histoplasmosis)
Side effects: Nausea, liver enzyme elevation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Posaconazole
Category: Antifungal (azole class)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 200–300 mg daily [general reference only]
Uses: Fungal infections, prophylaxis in immunocompromised
Side effects: Nausea, headache, liver enzyme elevation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Voriconazole
Category: Antifungal (azole class)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 200 mg twice daily [general reference only]
Uses: Invasive aspergillosis, candidiasis
Side effects: Visual disturbances, liver toxicity
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Amphotericin B liposomal
Category: Antifungal
Route: Intravenous
Storage: Refrigerate, protect from light
Typical dose: Adults 3–5 mg/kg daily [general reference only]
Uses: Severe fungal infections
Side effects: Kidney toxicity, fever, chills
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Cyclophosphamide
Category: Alkylating agent (anticancer, immunosuppressant)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 500–1500 mg/m² per cycle [general reference only]
Uses: Cancers, autoimmune diseases
Side effects: Bone marrow suppression, hair loss, bladder toxicity
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Cisplatin
Category: Platinum-based anticancer agent
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 50–100 mg/m² per cycle [general reference only]
Uses: Solid tumors (lung, ovarian, testicular)
Side effects: Kidney toxicity, nausea, hearing loss
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Carboplatin
Category: Platinum-based anticancer agent
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults individualized by renal function [general reference only]
Uses: Ovarian cancer, lung cancer
Side effects: Bone marrow suppression, nausea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Paclitaxel
Category: Anticancer (taxane)
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 135–175 mg/m² every 3 weeks [general reference only]
Uses: Breast, ovarian, lung cancers
Side effects: Hair loss, neuropathy, bone marrow suppression
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Docetaxel
Category: Anticancer (taxane)
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 60–100 mg/m² every 3 weeks [general reference only]
Uses: Breast, prostate, lung cancers
Side effects: Hair loss, neuropathy, fluid retention
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Doxorubicin
Category: Anticancer (anthracycline)
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 60–75 mg/m² per cycle [general reference only]
Uses: Breast cancer, lymphomas
Side effects: Heart toxicity, hair loss, nausea
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Epirubicin
Category: Anticancer (anthracycline)
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 60–120 mg/m² per cycle [general reference only]
Uses: Breast cancer
Side effects: Heart toxicity, hair loss, nausea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Bleomycin
Category: Anticancer (antibiotic)
Route: Intravenous, Intramuscular
Storage: Store below 25°C
Typical dose: Adults 10–20 units weekly [general reference only]
Uses: Testicular cancer, Hodgkin's lymphoma
Side effects: Lung toxicity, skin changes
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vincristine
Category: Anticancer (vinca alkaloid)
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 1.4 mg/m² weekly [general reference only]
Uses: Leukemia, lymphomas
Side effects: Neuropathy, constipation
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vinblastine
Category: Anticancer (vinca alkaloid)
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 6 mg/m² every 2 weeks [general reference only]
Uses: Hodgkin's lymphoma, testicular cancer
Side effects: Bone marrow suppression, hair loss
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Methadone
Category: Opioid analgesic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–40 mg daily [general reference only]
Uses: Pain management, opioid dependence
Side effects: Constipation, drowsiness, dependence risk
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Buprenorphine
Category: Partial opioid agonist
Route: Sublingual, Transdermal
Storage: Store below 25°C
Typical dose: Adults 2–24 mg daily [general reference only]
Uses: Opioid dependence, pain management
Side effects: Constipation, headache, withdrawal symptoms
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Naloxone
Category: Opioid antagonist
Route: Intravenous, Intramuscular, Intranasal
Storage: Store below 25°C
Typical dose: Adults 0.4–2 mg every 2–3 minutes as needed [general reference only]
Uses: Opioid overdose reversal
Side effects: Withdrawal symptoms, agitation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Naltrexone
Category: Opioid antagonist
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 50 mg once daily [general reference only]
Uses: Alcohol dependence, opioid dependence
Side effects: Nausea, headache, liver enzyme elevation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Acetazolamide
Category: Carbonic anhydrase inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 250–1000 mg daily [general reference only]
Uses: Glaucoma, altitude sickness, epilepsy
Side effects: Tingling, kidney stones, fatigue
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Levonorgestrel
Category: Progestin (contraceptive)
Route: Oral, Intrauterine
Storage: Store below 25°C
Typical dose: Oral 1.5 mg single dose (emergency contraception) [general reference only]
Uses: Birth control, emergency contraception
Side effects: Nausea, irregular bleeding
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ethinylestradiol
Category: Estrogen (contraceptive)
Route: Oral
Storage: Store below 25°C
Typical dose: Combined with progestin in contraceptive pills [general reference only]
Uses: Birth control, hormone therapy
Side effects: Nausea, breast tenderness, clot risk
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Medroxyprogesterone acetate
Category: Progestin
Route: Oral, Intramuscular
Storage: Store below 25°C
Typical dose: IM 150 mg every 3 months [general reference only]
Uses: Contraception, hormone therapy
Side effects: Weight gain, irregular bleeding
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Estradiol
Category: Estrogen
Route: Oral, Transdermal, Intramuscular
Storage: Store below 25°C
Typical dose: Adults 1–2 mg daily (oral) [general reference only]
Uses: Hormone replacement therapy
Side effects: Nausea, breast tenderness, clot risk
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Testosterone
Category: Androgen
Route: Intramuscular, Transdermal
Storage: Store below 25°C
Typical dose: Adults 50–100 mg IM every 1–2 weeks [general reference only]
Uses: Hypogonadism, hormone therapy
Side effects: Acne, mood changes, liver effects
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Finasteride
Category: 5-alpha reductase inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 1–5 mg daily [general reference only]
Uses: Benign prostatic hyperplasia, male pattern baldness
Side effects: Sexual dysfunction, breast tenderness
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tamsulosin
Category: Alpha-1 blocker
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 0.4 mg once daily [general reference only]
Uses: Benign prostatic hyperplasia
Side effects: Dizziness, ejaculation problems
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Sildenafil
Category: PDE-5 inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 25–100 mg as needed [general reference only]
Uses: Erectile dysfunction, pulmonary hypertension
Side effects: Headache, flushing, vision changes
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tadalafil
Category: PDE-5 inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–20 mg daily or as needed [general reference only]
Uses: Erectile dysfunction, pulmonary hypertension
Side effects: Headache, flushing, back pain
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Varenicline
Category: Nicotinic receptor partial agonist
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 0.5–1 mg twice daily [general reference only]
Uses: Smoking cessation
Side effects: Nausea, vivid dreams, mood changes
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Nicotine replacement therapy (patch)
Category: Nicotine agonist
Route: Transdermal
Storage: Store below 25°C
Typical dose: 21 mg patch daily [general reference only]
Uses: Smoking cessation
Side effects: Skin irritation, insomnia
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Levocetirizine
Category: Antihistamine
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5 mg once daily [general reference only]
Uses: Allergic rhinitis, urticaria
Side effects: Drowsiness, dry mouth
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Montelukast
Category: Leukotriene receptor antagonist
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10 mg once daily [general reference only]
Uses: Asthma, allergic rhinitis
Side effects: Headache, abdominal pain, mood changes
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Theophylline
Category: Bronchodilator (xanthine derivative)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 200–400 mg daily [general reference only]
Uses: Asthma, COPD
Side effects: Nausea, arrhythmias, insomnia
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Budesonide
Category: Corticosteroid
Route: Inhalation, Oral
Storage: Store below 25°C
Typical dose: Adults 200–800 mcg daily (inhalation) [general reference only]
Uses: Asthma, COPD
Side effects: Oral thrush, hoarseness
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Fluticasone
Category: Corticosteroid
Route: Inhalation, Nasal
Storage: Store below 25°C
Typical dose: Adults 100–500 mcg daily (inhalation) [general reference only]
Uses: Asthma, allergic rhinitis
Side effects: Oral thrush, nasal irritation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Beclomethasone
Category: Corticosteroid
Route: Inhalation
Storage: Store below 25°C
Typical dose: Adults 100–400 mcg daily [general reference only]
Uses: Asthma
Side effects: Oral thrush, hoarseness
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Mometasone
Category: Corticosteroid
Route: Inhalation, Nasal, Topical
Storage: Store below 25°C
Typical dose: Adults 200 mcg daily (inhalation) [general reference only]
Uses: Asthma, allergic rhinitis, skin inflammation
Side effects: Oral thrush, nasal irritation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Cromolyn sodium
Category: Mast cell stabilizer
Route: Inhalation, Nasal
Storage: Store below 25°C
Typical dose: Adults 20 mg inhaled 4 times daily [general reference only]
Uses: Asthma prevention, allergic rhinitis
Side effects: Throat irritation, cough
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ketamine
Category: Anesthetic
Route: Intravenous, Intramuscular
Storage: Store below 25°C
Typical dose: Adults 1–2 mg/kg IV [general reference only]
Uses: Anesthesia, pain management, depression (investigational)
Side effects: Hallucinations, increased blood pressure
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Propofol
Category: Anesthetic
Route: Intravenous
Storage: Store below 25°C
Typical dose: Adults 1–2 mg/kg IV induction [general reference only]
Uses: Anesthesia induction and maintenance
Side effects: Hypotension, respiratory depression
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Midazolam
Category: Benzodiazepine (sedative)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 1–5 mg IV [general reference only]
Uses: Sedation, anesthesia adjunct
Side effects: Drowsiness, respiratory depression
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Fentanyl
Category: Opioid analgesic
Route: Intravenous, Transdermal
Storage: Store below 25°C
Typical dose: Adults 25–100 mcg IV [general reference only]
Uses: Severe pain, anesthesia
Side effects: Respiratory depression, dependence risk
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tramadol
Category: Opioid analgesic
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 50–100 mg every 6 hours [general reference only]
Uses: Moderate pain
Side effects: Nausea, dizziness, dependence risk
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Celecoxib
Category: COX-2 inhibitor (NSAID)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100–200 mg daily [general reference only]
Uses: Arthritis, pain relief
Side effects: Stomach upset, cardiovascular risk
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Naproxen
Category: NSAID
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 250–500 mg twice daily [general reference only]
Uses: Pain, inflammation, arthritis
Side effects: Stomach upset, ulcers
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Indomethacin
Category: NSAID
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 25–50 mg 2–3 times daily [general reference only]
Uses: Arthritis, gout, pain
Side effects: Stomach upset, headache
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ketorolac
Category: NSAID
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 10–30 mg every 6 hours [general reference only]
Uses: Short-term pain relief
Side effects: Stomach upset, kidney effects
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Diclofenac
Category: NSAID
Route: Oral, Topical
Storage: Store below 25°C
Typical dose: Adults 50–75 mg twice daily [general reference only]
Uses: Pain, arthritis, inflammation
Side effects: Stomach upset, liver enzyme elevation
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Levetiracetam
Category: Anticonvulsant
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 500–3000 mg daily [general reference only]
Uses: Epilepsy
Side effects: Drowsiness, mood changes
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Phenytoin
Category: Anticonvulsant
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 300–400 mg daily [general reference only]
Uses: Epilepsy
Side effects: Gum overgrowth, dizziness, rash
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Valproic acid
Category: Anticonvulsant, mood stabilizer
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 600–2500 mg daily [general reference only]
Uses: Epilepsy, bipolar disorder
Side effects: Liver toxicity, weight gain, tremors
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Phenobarbital
Category: Barbiturate (anticonvulsant)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 60–240 mg daily [general reference only]
Uses: Epilepsy, sedation
Side effects: Drowsiness, dependence risk
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Zolpidem
Category: Hypnotic (sleep aid)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–10 mg at bedtime [general reference only]
Uses: Insomnia
Side effects: Drowsiness, dizziness, sleepwalking
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Eszopiclone
Category: Hypnotic (sleep aid)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 1–3 mg at bedtime [general reference only]
Uses: Insomnia
Side effects: Drowsiness, metallic taste
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ramelteon
Category: Melatonin receptor agonist
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 8 mg at bedtime [general reference only]
Uses: Insomnia
Side effects: Drowsiness, dizziness
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Melatonin
Category: Hormone (sleep aid)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 1–5 mg at bedtime [general reference only]
Uses: Insomnia, jet lag
Side effects: Drowsiness, headache
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Desmopressin
Category: Synthetic vasopressin analog
Route: Oral, Intranasal, Intravenous
Storage: Store below 25°C
Typical dose: Adults 0.1–0.4 mg daily [general reference only]
Uses: Diabetes insipidus, bedwetting
Side effects: Low sodium, headache
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Latanoprost
Category: Prostaglandin analog (ophthalmic)
Route: Ophthalmic drops
Storage: Refrigerate before opening, then room temp
Typical dose: 1 drop once daily [general reference only]
Uses: Glaucoma, ocular hypertension
Side effects: Eye redness, eyelash growth
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Timolol
Category: Beta-blocker (ophthalmic)
Route: Ophthalmic drops
Storage: Store below 25°C
Typical dose: 1 drop twice daily [general reference only]
Uses: Glaucoma
Side effects: Eye irritation, bradycardia
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Brimonidine
Category: Alpha-2 agonist (ophthalmic)
Route: Ophthalmic drops
Storage: Store below 25°C
Typical dose: 1 drop twice daily [general reference only]
Uses: Glaucoma
Side effects: Eye redness, dry mouth
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Dorzolamide
Category: Carbonic anhydrase inhibitor (ophthalmic)
Route: Ophthalmic drops
Storage: Store below 25°C
Typical dose: 1 drop twice daily [general reference only]
Uses: Glaucoma
Side effects: Eye stinging, bitter taste
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Pilocarpine
Category: Cholinergic agonist (ophthalmic)
Route: Ophthalmic drops
Storage: Store below 25°C
Typical dose: 1 drop 3–4 times daily [general reference only]
Uses: Glaucoma
Side effects: Blurred vision, headache
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Isotretinoin
Category: Retinoid
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 0.5–1 mg/kg daily [general reference only]
Uses: Severe acne
Side effects: Birth defects, dry skin, mood changes
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Adapalene
Category: Retinoid (topical)
Route: Topical
Storage: Store below 25°C
Typical dose: Apply once daily [general reference only]
Uses: Acne
Side effects: Skin irritation, dryness
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Clobetasol
Category: Corticosteroid (topical)
Route: Topical
Storage: Store below 25°C
Typical dose: Apply thin layer once or twice daily [general reference only]
Uses: Psoriasis, eczema
Side effects: Skin thinning, irritation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Calcipotriol
Category: Vitamin D analog (topical)
Route: Topical
Storage: Store below 25°C
Typical dose: Apply once or twice daily [general reference only]
Uses: Psoriasis
Side effects: Skin irritation
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Tacrolimus (topical)
Category: Calcineurin inhibitor
Route: Topical
Storage: Store below 25°C
Typical dose: Apply twice daily [general reference only]
Uses: Eczema, dermatitis
Side effects: Burning sensation, skin irritation
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Pantoprazole
Category: Proton Pump Inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 40 mg once daily [general reference only]
Uses: GERD, ulcers
Side effects: Headache, diarrhea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Rabeprazole
Category: Proton Pump Inhibitor
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 20 mg once daily [general reference only]
Uses: GERD, ulcers
Side effects: Headache, diarrhea
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Sucralfate
Category: Gastroprotective agent
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 1 g four times daily [general reference only]
Uses: Ulcers
Side effects: Constipation, dry mouth
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Loperamide
Category: Antidiarrheal
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 2–4 mg initially, then 2 mg after each loose stool [general reference only]
Uses: Diarrhea
Side effects: Constipation, abdominal pain
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Ondansetron
Category: Antiemetic (5-HT3 antagonist)
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 4–8 mg every 8 hours [general reference only]
Uses: Nausea, vomiting
Side effects: Headache, constipation
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Metoclopramide
Category: Antiemetic, prokinetic
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 10 mg three times daily [general reference only]
Uses: Nausea, gastroparesis
Side effects: Drowsiness, movement disorders
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Domperidone
Category: Antiemetic, prokinetic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 10 mg three times daily [general reference only]
Uses: Nausea, vomiting
Side effects: Headache, QT prolongation
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vitamin A
Category: Fat-soluble vitamin
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 700–900 mcg daily [general reference only]
Uses: Deficiency, eye health
Side effects: Toxicity at high doses
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vitamin D (Cholecalciferol)
Category: Fat-soluble vitamin
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 600–2000 IU daily [general reference only]
Uses: Bone health, deficiency
Side effects: High calcium levels
Citation: WHO Essential Medicines List, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vitamin E
Category: Fat-soluble vitamin
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 15 mg daily [general reference only]
Uses: Deficiency, antioxidant
Side effects: Bleeding risk at high doses
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Vitamin K
Category: Fat-soluble vitamin
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 1–10 mg daily [general reference only]
Uses: Clotting disorders, deficiency
Side effects: Injection site reactions
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Human Papillomavirus (HPV) vaccine
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: 2–3 doses depending on age [general reference only]
Uses: Prevention of HPV infection, cervical cancer
Side effects: Injection site pain, fever
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hepatitis B vaccine
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: 3 doses [general reference only]
Uses: Prevention of Hepatitis B
Side effects: Injection site pain, mild fever
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Influenza vaccine
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: Annual dose [general reference only]
Uses: Prevention of influenza
Side effects: Injection site pain, mild fever
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Measles, Mumps, Rubella (MMR) vaccine
Category: Vaccine
Route: Subcutaneous
Storage: Refrigerate at 2–8°C
Typical dose: 2 doses [general reference only]
Uses: Prevention of measles, mumps, rubella
Side effects: Fever, rash
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Polio vaccine (IPV)
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: 4 doses [general reference only]
Uses: Prevention of poliomyelitis
Side effects: Injection site pain
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Diphtheria-Tetanus-Pertussis (DTaP) vaccine
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: 5 doses [general reference only]
Uses: Prevention of diphtheria, tetanus, pertussis
Side effects: Fever, injection site pain
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Varicella vaccine
Category: Vaccine
Route: Subcutaneous
Storage: Refrigerate at 2–8°C
Typical dose: 2 doses [general reference only]
Uses: Prevention of chickenpox
Side effects: Rash, fever
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Rotavirus vaccine
Category: Vaccine
Route: Oral
Storage: Refrigerate at 2–8°C
Typical dose: 2–3 doses [general reference only]
Uses: Prevention of rotavirus diarrhea
Side effects: Irritability, mild diarrhea
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Pneumococcal vaccine
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: 1–4 doses depending on age [general reference only]
Uses: Prevention of pneumococcal infections
Side effects: Injection site pain, fever
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Rabies vaccine
Category: Vaccine
Route: Intramuscular
Storage: Refrigerate at 2–8°C
Typical dose: 4–5 doses [general reference only]
Uses: Prevention of rabies
Side effects: Injection site pain, headache
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Iron (Ferrous sulfate)
Category: Mineral supplement
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 100–200 mg elemental iron daily [general reference only]
Uses: Iron deficiency anemia
Side effects: Constipation, dark stools
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Folic acid
Category: Vitamin (B9)
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 400 mcg daily [general reference only]
Uses: Anemia prevention, pregnancy supplementation
Side effects: Rare, mild GI upset
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Calcium carbonate
Category: Mineral supplement
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 500–1500 mg daily [general reference only]
Uses: Calcium deficiency, osteoporosis prevention
Side effects: Constipation, kidney stones
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Magnesium sulfate
Category: Mineral supplement
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 1–2 g IV [general reference only]
Uses: Eclampsia, hypomagnesemia
Side effects: Flushing, low blood pressure
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Potassium chloride
Category: Electrolyte supplement
Route: Oral, Intravenous
Storage: Store below 25°C
Typical dose: Adults 20–100 mEq daily [general reference only]
Uses: Hypokalemia
Side effects: GI upset, arrhythmias (if overdosed)
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Liothyronine
Category: Thyroid hormone
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 25–75 mcg daily [general reference only]
Uses: Hypothyroidism
Side effects: Palpitations, insomnia
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hydrocodone
Category: Opioid analgesic
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 5–10 mg every 4–6 hours [general reference only]
Uses: Moderate pain
Side effects: Constipation, drowsiness, dependence risk
Citation: FDA Drug Database, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Codeine
Category: Opioid analgesic, antitussive
Route: Oral
Storage: Store below 25°C
Typical dose: Adults 15–60 mg every 4–6 hours [general reference only]
Uses: Pain, cough suppression
Side effects: Constipation, drowsiness, dependence risk
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Chlorhexidine
Category: Antiseptic
Route: Topical, Oral rinse
Storage: Store below 25°C
Typical dose: Mouth rinse 10–15 ml twice daily [general reference only]
Uses: Skin disinfection, oral hygiene
Side effects: Staining of teeth, irritation
Citation: WHO Essential Medicines List, FDA
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Hydrogen peroxide
Category: Antiseptic
Route: Topical
Storage: Store below 25°C
Typical dose: Apply externally as needed [general reference only]
Uses: Wound cleaning
Side effects: Skin irritation
Citation: PubMed, FDA Drug Database
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.

Drug common name: Povidone-iodine
Category: Antiseptic
Route: Topical
Storage: Store below 25°C
Typical dose: Apply externally as needed [general reference only]
Uses: Skin disinfection
Side effects: Skin irritation, iodine absorption
Citation: WHO Essential Medicines List, PubMed
Disclaimer: This information is for educational purposes only. For personal medical advice, consult a licensed doctor.
"""

def parse_drugs_from_text(text):
    """Parse drug data from raw text format"""
    drugs = []
    
    # Split by "Drug common name:" to get individual drug blocks
    blocks = text.split("Drug common name:")[1:]  # Skip the first empty split
    
    for block in blocks:
        lines = block.strip().split("\n")
        drug_data = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith("Drug common name:"):
                drug_data["Drug"] = line.replace("Drug common name:", "").strip()
            elif line.startswith("Category:"):
                drug_data["Category"] = line.replace("Category:", "").strip()
            elif line.startswith("Route:"):
                drug_data["Route"] = line.replace("Route:", "").strip()
            elif line.startswith("Storage:"):
                drug_data["Storage"] = line.replace("Storage:", "").strip()
            elif line.startswith("Typical dose:"):
                drug_data["Dose"] = line.replace("Typical dose:", "").strip()
            elif line.startswith("Uses:"):
                # Split by commas and clean up
                uses_str = line.replace("Uses:", "").strip()
                drug_data["Uses"] = [u.strip() for u in uses_str.split(",")]
            elif line.startswith("Side effects:"):
                # Split by commas and clean up
                effects_str = line.replace("Side effects:", "").strip()
                drug_data["Side Effects"] = [e.strip() for e in effects_str.split(",")]
            elif line.startswith("Citation:"):
                drug_data["Citation"] = line.replace("Citation:", "").strip()
            elif line.startswith("Disclaimer:"):
                drug_data["Disclaimer"] = line.replace("Disclaimer:", "").strip()
        
        # Only add if we have the minimum required fields
        if "Drug" in drug_data and len(drug_data) > 2:
            # Set defaults for missing fields
            if "Category" not in drug_data:
                drug_data["Category"] = "Not specified"
            if "Route" not in drug_data:
                drug_data["Route"] = "Not specified"
            if "Storage" not in drug_data:
                drug_data["Storage"] = "Below 25°C"
            if "Dose" not in drug_data:
                drug_data["Dose"] = "As directed"
            if "Uses" not in drug_data:
                drug_data["Uses"] = ["Not specified"]
            if "Side Effects" not in drug_data:
                drug_data["Side Effects"] = ["Rare or none specified"]
            if "Citation" not in drug_data:
                drug_data["Citation"] = "General reference"
            if "Disclaimer" not in drug_data:
                drug_data["Disclaimer"] = "Educational use only. Consult a physician for medical advice."
            
            drugs.append(drug_data)
    
    return drugs

# Parse the drugs
parsed_drugs = parse_drugs_from_text(raw_drugs_text)

# Load existing drugs
pharmacopoeia_path = "pharmacopoeia.json"
with open(pharmacopoeia_path, "r", encoding="utf-8") as f:
    try:
        existing_drugs = json.load(f)
    except json.JSONDecodeError:
        existing_drugs = []

# Create a set of existing drug names for deduplication (case-insensitive)
existing_names = {drug["Drug"].lower() for drug in existing_drugs}

# Add new drugs, avoiding duplicates
new_count = 0
for drug in parsed_drugs:
    drug_name_lower = drug["Drug"].lower()
    if drug_name_lower not in existing_names:
        existing_drugs.append(drug)
        existing_names.add(drug_name_lower)
        new_count += 1

# Save the updated database
with open(pharmacopoeia_path, "w", encoding="utf-8") as f:
    json.dump(existing_drugs, f, indent=2, ensure_ascii=False)

print(f"✓ Import complete!")
print(f"✓ Added {new_count} new drugs")
print(f"✓ Total drugs in database: {len(existing_drugs)}")
