import csv

file_path = "data/wearable/wearable_data.csv"

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print("Number of wearable records:", len(rows))

print("\nFirst 5 records:")
for row in rows[:5]:
    print(row)