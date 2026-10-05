import json
import csv
from pathlib import Path

ehr_folder = Path("data/ehr")
output_file = Path("data/ehr_patient.csv")

files = list(ehr_folder.glob("*.json"))

with open(files[0], "r", encoding="utf-8") as f:
    bundle = json.load(f)

patient = None
conditions = []

for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})
    resource_type = resource.get("resourceType")

    if resource_type == "Patient":
        patient = resource

    elif resource_type == "Condition":
        text = resource.get("code", {}).get("text", "")
        conditions.append(text)

# Basic patient information
birth_date = patient.get("birthDate")
gender = patient.get("gender")

# Cardiovascular measurements
weights = []
bmis = []
heart_rates = []
cholesterol = []
ldl = []
hdl = []
triglycerides = []

for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})

    if resource.get("resourceType") != "Observation":
        continue

    name = resource.get("code", {}).get("text", "")
    value = resource.get("valueQuantity", {}).get("value")

    if value is None:
        continue

    if name == "Body Weight":
        weights.append(value)
    elif "Body mass index" in name:
        bmis.append(value)
    elif name == "Heart rate":
        heart_rates.append(value)
    elif name == "Cholesterol [Mass/volume] in Serum or Plasma":
        cholesterol.append(value)
    elif "Cholesterol in LDL" in name:
        ldl.append(value)
    elif "Cholesterol in HDL" in name:
        hdl.append(value)
    elif name == "Triglyceride [Mass/volume] in Serum or Plasma":
        triglycerides.append(value)

# Relevant conditions
has_hypertension = any(
    "hypertension" in c.lower() for c in conditions
)

has_obesity = any(
    "obesity" in c.lower() for c in conditions
)

row = {
    "patient_id": patient.get("id"),
    "gender": gender,
    "birth_date": birth_date,
    "hypertension": int(has_hypertension),
    "obesity_history": int(has_obesity),

    "baseline_weight_kg": round(sum(weights) / len(weights), 2) if weights else None,
    "baseline_bmi": round(sum(bmis) / len(bmis), 2) if bmis else None,
    "baseline_heart_rate": round(sum(heart_rates) / len(heart_rates), 2) if heart_rates else None,
    "baseline_cholesterol": round(sum(cholesterol) / len(cholesterol), 2) if cholesterol else None,
    "baseline_ldl": round(sum(ldl) / len(ldl), 2) if ldl else None,
    "baseline_hdl": round(sum(hdl) / len(hdl), 2) if hdl else None,
    "baseline_triglycerides": round(sum(triglycerides) / len(triglycerides), 2) if triglycerides else None,
}

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    writer.writeheader()
    writer.writerow(row)

print("EHR dataset created!")
print(output_file)
print(row)