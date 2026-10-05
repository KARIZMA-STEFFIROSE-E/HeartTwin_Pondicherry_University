import csv
import random
from datetime import date, timedelta

output_file = "data/wearable/wearable_data.csv"

random.seed(42)

patients = [
    "PATIENT_001",
    "PATIENT_002",
    "PATIENT_003",
    "PATIENT_004",
    "PATIENT_005",
    "PATIENT_006",
    "PATIENT_007",
    "PATIENT_008",
    "PATIENT_009",
    "PATIENT_010"
]

# Patients with different deterioration patterns
deterioration_patterns = {
    "PATIENT_002": "cardiac",
    "PATIENT_003": "sleep_activity",
    "PATIENT_005": "weight",
    "PATIENT_007": "mixed",
    "PATIENT_009": "hrv"
}

start_date = date.today() - timedelta(days=29)

with open(output_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "patient_id",
        "date",
        "resting_hr",
        "hrv",
        "sleep_hours",
        "steps",
        "spo2",
        "weight_kg"
    ])

    for patient_id in patients:

        # Personal baseline
        base_hr = random.uniform(65, 80)
        base_hrv = random.uniform(40, 70)
        base_sleep = random.uniform(6.5, 8)
        base_steps = random.uniform(5000, 9000)
        base_spo2 = random.uniform(96, 99)
        base_weight = random.uniform(60, 90)

        pattern = deterioration_patterns.get(patient_id)

        for day in range(30):

            current_date = start_date + timedelta(days=day)

            # Normal daily variation
            resting_hr = random.gauss(base_hr, 3)
            hrv = random.gauss(base_hrv, 7)
            sleep = random.gauss(base_sleep, 0.6)
            steps = random.gauss(base_steps, 1000)
            spo2 = random.gauss(base_spo2, 0.7)
            weight = random.gauss(base_weight, 0.5)

            # Deterioration begins after day 22
            if pattern and day >= 23:

                severity = day - 22

                if pattern == "cardiac":
                    resting_hr += severity * 2.0
                    hrv -= severity * 2.5
                    spo2 -= severity * 0.15

                elif pattern == "sleep_activity":
                    sleep -= severity * 0.25
                    steps -= severity * 600
                    resting_hr += severity * 1.2

                elif pattern == "weight":
                    weight += severity * 0.45
                    resting_hr += severity * 1.0
                    steps -= severity * 300

                elif pattern == "mixed":
                    resting_hr += severity * 1.5
                    hrv -= severity * 2.5
                    sleep -= severity * 0.18
                    steps -= severity * 450
                    spo2 -= severity * 0.20
                    weight += severity * 0.25

                elif pattern == "hrv":
                    hrv -= severity * 3.0
                    resting_hr += severity * 1.0
                    sleep -= severity * 0.15

            writer.writerow([
                patient_id,
                current_date,
                round(resting_hr, 1),
                round(max(hrv, 10), 1),
                round(max(sleep, 3), 1),
                round(max(steps, 1000)),
                round(min(max(spo2, 90), 100), 1),
                round(weight, 1)
            ])

print("Wearable dataset created!")
print("Patients:", len(patients))
print("Days per patient:", 30)
print("Total records:", len(patients) * 30)

print("\nDeterioration patients:")
for patient, pattern in deterioration_patterns.items():
    print(patient, "->", pattern)

print("\nOutput:")
print(output_file)