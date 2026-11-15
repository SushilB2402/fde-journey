import os
import random
import json
from pathlib import Path
import pandas as pd

# Fix the path to build from its own location
DATA = Path(__file__).parent / "data"
DATA.mkdir(parents=True, exist_ok=True)

random.seed(42)

N = 300
# Generate 300 unique IDs so there are no accidental background duplicates
ids = random.sample(range(1000, 9999), N)

order = list(range(N))
random.shuffle(order)

def take(k):
    return [order.pop() for _ in range(k)]

# Initialize background clean rows
appointments = []
for i in range(N):
    appointments.append({
        "appointment_id": str(ids[i]),
        "clinic": "Cardiology",
        "date": "01/03/2026",
        "status": "Completed",
        "fee": "100.00"
    })

planted_counts = {
    "total_rows": N,
    "blank_id": 0,
    "duplicate_id": 0,
    "impossible_date": 0,
    "blank_date": 0,
    "unknown_status": 0,
    "unknown_clinic": 0,
    "negative_fee": 0,
    "blank_fee": 0
}

# 1. Blank IDs
idx_list = take(12)
for idx in idx_list:
    appointments[idx]["appointment_id"] = ""
    planted_counts["blank_id"] += 1

# 2. Duplicate IDs (copy an existing ID from another row)
# Reserve 15 pristine source rows via take(), so a source can never be blank or
# carry another flaw. Each duplicate then copies the ID of its own clean source.
dup_rows = take(15)
source_rows = take(15)
for idx, source_idx in zip(dup_rows, source_rows):
    appointments[idx]["appointment_id"] = appointments[source_idx]["appointment_id"]
    planted_counts["duplicate_id"] += 1

# 3. Truly impossible dates from a fixed list
impossible_dates_list = ["31/04/2026", "31/06/2026", "31/09/2026", "31/11/2026", "30/02/2026", "31/02/2026", "29/02/2025"]
idx_list = take(10)
for idx in idx_list:
    appointments[idx]["date"] = random.choice(impossible_dates_list)
    planted_counts["impossible_date"] += 1

# 4. Blank dates
idx_list = take(8)
for idx in idx_list:
    appointments[idx]["date"] = ""
    planted_counts["blank_date"] += 1

# 5. Unknown status
idx_list = take(18)
for idx in idx_list:
    appointments[idx]["status"] = "Pending"
    planted_counts["unknown_status"] += 1

# 6. Unknown clinic
idx_list = take(14)
for idx in idx_list:
    appointments[idx]["clinic"] = "Unknown Clinic"
    planted_counts["unknown_clinic"] += 1

# 7. Negative fee
idx_list = take(8)
for idx in idx_list:
    appointments[idx]["fee"] = "-50.00"
    planted_counts["negative_fee"] += 1

# 8. Blank fee
idx_list = take(10)
for idx in idx_list:
    appointments[idx]["fee"] = ""
    planted_counts["blank_fee"] += 1

# Cleanable noise (variants, £ signs, stray spaces, mixed date formats)
clinics_variants = [" cardio outpatients", "Ortho", "Derm"]
statuses_variants = ["no show", "No-Show", "Cancelled"]

for i in range(N):
    if appointments[i]["fee"] != "":
        if random.random() < 0.45:
            appointments[i]["fee"] = f"£{appointments[i]['fee']}"
            
    if appointments[i]["clinic"] == "Cardiology" and random.random() < 0.3:
        appointments[i]["clinic"] = random.choice(clinics_variants)
    if appointments[i]["status"] == "Completed" and random.random() < 0.3:
        appointments[i]["status"] = random.choice(statuses_variants)
        
    if appointments[i]["date"] != "" and random.random() < 0.5:
        dt = pd.to_datetime(appointments[i]["date"], format="%d/%m/%Y", errors="coerce")
        if pd.notna(dt):
            appointments[i]["date"] = dt.strftime("%Y-%m-%d")
            
    if random.random() < 0.2:
        appointments[i]["clinic"] = f"   {appointments[i]['clinic']} "
    if random.random() < 0.2:
        appointments[i]["status"] = f" {appointments[i]['status']}  "

df_messy = pd.DataFrame(appointments)
csv_path = DATA / "appointments_messy.csv"
df_messy.to_csv(csv_path, index=False)

# Inject intentional blank lines into the CSV file to test independent row counting
with open(csv_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for idx, line in enumerate(lines):
    new_lines.append(line)
    if idx in [15, 45, 100, 200]:
        new_lines.append("\n")

with open(csv_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# Write planted_counts.json to data folder
json_path = DATA / "planted_counts.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(planted_counts, f, indent=4)

print("Planted counts written to JSON successfully:", planted_counts)