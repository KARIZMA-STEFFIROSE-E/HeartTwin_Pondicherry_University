import csv
import random

output_file = "data/ehr_patient_profiles.csv"

random.seed(42)

patients = []

for i in range(1, 11):

    patient_id = f"PATIENT_{i:03d}"

    age = random.randint(40, 75)
    sex = random.choice(["male", "female"])

    hypertension = random.choice([0, 0, 1])
    diabetes = random.choice([0, 0, 1])
    smoking = random.choice([0, 0, 1])
    previous_cardiac_event = random.choice([0, 0, 0, 1])

    bmi = round(random.uniform(22, 34), 1)
    cholesterol = round(random.uniform(150, 240), 1)

    patients.append([
        patient_id,
        age,
        sex,
        bmi,
        hypertension,
        diabetes,
        smoking,
        previous_cardiac_event,
        cholesterol
    ])

with open(output_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "patient_id",
        "age",
        "sex",
        "bmi",
        "hypertension",
        "diabetes",
        "smoking",
        "previous_cardiac_event",
        "cholesterol"
    ])

    writer.writerows(patients)

print("EHR profiles created!")
print("Patients:", len(patients))
print(output_file)