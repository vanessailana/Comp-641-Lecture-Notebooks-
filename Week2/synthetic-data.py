import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

NUM_ROWS = 300
OUTPUT_PATH = "covid_clinical_notes_synthetic.csv"

np.random.seed(42)
random.seed(42)

first_names = ["John", "Maria", "David", "Emily", "Ahmed", "Sophia", "James", "Anna", "Luis", "Grace"]
last_names = ["Smith", "Lopez", "Kim", "Patel", "Johnson", "Chen", "Ali", "Garcia", "Brown", "Nguyen"]
cities = ["Glendale", "Burbank", "Pasadena", "Los Angeles", "Santa Monica", "Long Beach"]
zip_codes = ["91203", "91502", "91104", "90024", "90401", "90802"]
hospitals = ["St. Mary's Medical Center", "Valley General Hospital", "Eastside Community Hospital",
             "Westbrook Medical Center", "North Hills Clinic"]
providers = ["Dr. Emily Chen", "Dr. Jason Lee", "Dr. Sarah Patel", "Dr. Michael Brown", "Dr. Anna Garcia", "Dr. David Kim"]
sexes = ["Male", "Female", "Other"]
covid_results = ["Positive", "Negative", "Pending"]
icu_options = ["Yes", "No"]
comorbidity_pool = ["hypertension", "diabetes", "obesity", "asthma", "copd", "ckd", "none"]

base_date = datetime(2020, 3, 1)

def random_phone():
    area = random.choice(["818", "747", "310", "626"])
    return f"{area}-555-{random.randint(1000, 9999)}"

def random_comorbidities():
    k = np.random.choice([1, 1, 2, 2, 3])
    return ";".join(sorted(set(random.sample(comorbidity_pool, k))))

def make_note(row):
    return (
        f"{row['patient_name']} ({row['age']} y/o {row['sex'].lower()} from {row['city']} ZIP {row['zip_code']}) "
        f"was admitted to {row['hospital_name']} on {row['admission_date']} and evaluated by {row['provider_name']}. "
        f"Contact: {row['phone_number']}. Oxygen = {row['oxygen_saturation']}%, Temp = {row['temperature_c']} °C."
    )

rows = []
for i in range(NUM_ROWS):
    patient_id = f"P{str(i // 3 + 1).zfill(4)}"
    encounter_id = f"E{1000 + i}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = np.random.randint(18, 90)
    sex = random.choice(sexes)
    city = random.choice(cities)
    zip_code = random.choice(zip_codes)
    phone = random_phone()
    admit_date = base_date + timedelta(days=np.random.randint(0, 120))
    discharge_date = admit_date + timedelta(days=np.random.randint(1, 10))
    hospital = random.choice(hospitals)
    provider = random.choice(providers)
    covid_result = random.choice(covid_results)
    icu_admission = random.choice(icu_options)
    oxygen = round(np.random.normal(94, 4), 1)
    temp = round(np.random.normal(37.6, 0.8), 1)
    comorbidities = random_comorbidities()

    row = {
        "patient_id": patient_id,
        "encounter_id": encounter_id,
        "patient_name": name,
        "age": age,
        "sex": sex,
        "city": city,
        "zip_code": zip_code,
        "phone_number": phone,
        "admission_date": admit_date.strftime("%Y-%m-%d"),
        "discharge_date": discharge_date.strftime("%Y-%m-%d"),
        "hospital_name": hospital,
        "provider_name": provider,
        "covid_test_result": covid_result,
        "icu_admission": icu_admission,
        "oxygen_saturation": oxygen,
        "temperature_c": temp,
        "comorbidities": comorbidities,
    }
    row["note_text"] = make_note(row)
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_PATH, index=False)
print(f"Dataset saved as {OUTPUT_PATH}. Shape: {df.shape}")
