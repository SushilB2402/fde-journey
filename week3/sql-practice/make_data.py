import os
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_data():
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    random.seed(42)
    
    # 1. Sites Data (3 sites across regions)
    sites = [
        (1, "North Campus Medical Center", "North"),
        (2, "Downtown Health Plaza", "Central"),
        (3, "Westside Community Clinic Hub", "West")
    ]
    
    # 2. Clinics Data (including Clinic ID 106 as Empty Clinic Hub, and specialty column)
    clinics = [
        (101, 1, "General Pediatrics", "Pediatrics"),
        (102, 1, "Adult Primary Care", "General Practice"),
        (103, 2, "Downtown Cardiology", "Cardiology"),
        (104, 2, "Metro Dermatology", "Dermatology"),
        (105, 3, "Westside Orthopedics", "Orthopedics"),
        (106, 3, "Empty Clinic Hub", "General Practice")  # Zero appointments
    ]
    
    # Write sites.csv with plain utf-8 (avoiding BOM)
    with open(data_dir / "sites.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["site_id", "site_name", "region"])
        writer.writerows(sites)
        
    # Write clinics.csv with plain utf-8
    with open(data_dir / "clinics.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["clinic_id", "site_id", "clinic_name", "specialty"])
        writer.writerows(clinics)
        
    # 3. Appointments Data (~1000 appointments, per-clinic status probabilities)
    active_clinics = [c for c in clinics if c[0] != 106]
    
    # Per-clinic no-show rate definition
    NO_SHOW_RATE = {
        101: 0.10,
        102: 0.25,
        103: 0.05,
        104: 0.35,
        105: 0.20
    }
    
    appointments = []
    start_date = datetime(2026, 1, 1)
    
    appt_id = 1001
    for _ in range(1000):
        clinic = random.choice(active_clinics)
        clinic_id = clinic[0]
        patient_id = random.randint(5000, 5200)
        
        # Date range Jan 1 to Apr 1, 2026
        days_offset = random.randint(0, 90)
        appt_date = start_date + timedelta(days=days_offset, hours=random.randint(8, 17))
        
        # Status determination based on per-clinic no-show rate
        r = random.random()
        rate = NO_SHOW_RATE[clinic_id]
        if r < rate:
            status = "No-Show"
        elif r < rate + 0.10:
            status = "Cancelled"
        else:
            status = "Completed"
            
        fee = round(random.uniform(100.0, 250.0), 2)
        
        appointments.append((
            appt_id,
            patient_id,
            clinic_id,
            appt_date.strftime("%Y-%m-%d %H:%M:%S"),
            status,
            fee
        ))
        appt_id += 1
        
    # Write appointments.csv with plain utf-8
    with open(data_dir / "appointments.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["appointment_id", "patient_id", "clinic_id", "appointment_date", "status", "fee"])
        writer.writerows(appointments)
        
    print(f"Successfully generated synthetic dataset (~1000 appointments) in {data_dir}")

if __name__ == "__main__":
    generate_data()