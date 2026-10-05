import csv

input_file = "data/wearable/wearable_data.csv"
output_file = "data/wearable/wearable_labeled.csv"

# Patients that have simulated deterioration
deterioration_patients = {
    "PATIENT_002",
    "PATIENT_003",
    "PATIENT_005",
    "PATIENT_007",
    "PATIENT_009"
}

with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

fieldnames = reader.fieldnames + ["deterioration"]

for row in rows:

    patient_id = row["patient_id"]

    # Deterioration starts from day 23
    # Each patient's simulator creates deterioration
    # during the final 7 days.
    if patient_id in deterioration_patients:

        current_date = row["date"]

        # The simulator starts 29 days before today.
        # We identify the final 7 days using the row position
        # within each patient's 30-day sequence.

        patient_rows = [
            r for r in rows
            if r["patient_id"] == patient_id
        ]

        row_index = patient_rows.index(row)

        if row_index >= 23:
            row["deterioration"] = 1
        else:
            row["deterioration"] = 0

    else:
        row["deterioration"] = 0


with open(output_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows)


print("Labeled wearable dataset created!")
print("Total records:", len(rows))

print("\nDeterioration patients:")
for patient in sorted(deterioration_patients):
    print(patient)

print("\nDeterioration records:", sum(
    int(row["deterioration"]) for row in rows
))

print("\nOutput:")
print(output_file)