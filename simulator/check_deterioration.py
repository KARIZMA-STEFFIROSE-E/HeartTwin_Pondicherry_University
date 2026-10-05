import csv

file_path = "data/wearable/wearable_data.csv"

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for patient_id in ["PATIENT_003", "PATIENT_007"]:

    patient_rows = [
        row for row in rows
        if row["patient_id"] == patient_id
    ]

    print("\n", patient_id)

    print("First 3 days:")
    for row in patient_rows[:3]:
        print(row)

    print("\nLast 7 days:")
    for row in patient_rows[-7:]:
        print(row)