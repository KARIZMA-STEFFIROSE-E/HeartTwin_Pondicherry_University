import json
from pathlib import Path

ehr_folder = Path("data/ehr")
files = list(ehr_folder.glob("*.json"))

with open(files[0], "r", encoding="utf-8") as f:
    bundle = json.load(f)

print("Resource type:", bundle.get("resourceType"))
print("Bundle entries:", len(bundle.get("entry", [])))

for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})

    if resource.get("resourceType") == "Patient":
        patient = resource

        print("\nPATIENT FOUND!")
        print("ID:", patient.get("id"))
        print("Gender:", patient.get("gender"))
        print("Birth date:", patient.get("birthDate"))
        break

print("\nPATIENT CONDITIONS:")

print("\nCARDIOVASCULAR EHR DATA:")

keywords = [
    "Body Weight",
    "Body mass index",
    "Heart rate",
    "Cholesterol [Mass/volume]",
    "Cholesterol in LDL",
    "Cholesterol in HDL",
    "Triglyceride"
]

for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})

    if resource.get("resourceType") == "Observation":
        name = resource.get("code", {}).get("text", "")

        for keyword in keywords:
            if keyword in name:
                value = resource.get("valueQuantity", {})
                print(
                    f"- {name}: "
                    f"{value.get('value')} "
                    f"{value.get('unit', '')}"
                )
                break

count = 0

for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})

    if resource.get("resourceType") == "Observation":
        code = resource.get("code", {})
        name = code.get("text")

        value = resource.get("valueQuantity", {})
        value_number = value.get("value")
        unit = value.get("unit")

        if name and value_number is not None:
            print(f"- {name}: {value_number} {unit or ''}")
            count += 1

print("\nTotal observations:", count)