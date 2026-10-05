import csv

file_path = "data/wearable/wearable_labeled.csv"

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

normal = 0
deterioration = 0

for row in rows:

    if row["deterioration"] == "1":
        deterioration += 1
    else:
        normal += 1

print("Total records:", len(rows))
print("Normal records:", normal)
print("Deterioration records:", deterioration)