import os
import csv
import sqlite3
from pathlib import Path

def load_database():
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    db_path = base_dir / "healthcare.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key enforcement
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute("""
    CREATE TABLE sites (
        site_id INTEGER PRIMARY KEY,
        site_name TEXT NOT NULL,
        region TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE clinics (
        clinic_id INTEGER PRIMARY KEY,
        site_id INTEGER NOT NULL,
        clinic_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        FOREIGN KEY (site_id) REFERENCES sites (site_id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE appointments (
        appointment_id INTEGER PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        clinic_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        status TEXT NOT NULL,
        fee REAL NOT NULL,
        FOREIGN KEY (clinic_id) REFERENCES clinics (clinic_id)
    );
    """)
    
    # Independent CSV line counts (excluding header line)
    csv_counts = {}
    csv_files = {
        "sites": data_dir / "sites.csv",
        "clinics": data_dir / "clinics.csv",
        "appointments": data_dir / "appointments.csv"
    }
    
    for table, path in csv_files.items():
        with open(path, "r", encoding="utf-8-sig") as f:
            line_count = sum(1 for _ in f) - 1
            csv_counts[table] = line_count
            
    # Load sites.csv
    with open(csv_files["sites"], "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [(int(r["site_id"]), r["site_name"], r["region"]) for r in reader]
        cursor.executemany("INSERT INTO sites VALUES (?, ?, ?);", rows)
            
    # Load clinics.csv
    with open(csv_files["clinics"], "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [(int(r["clinic_id"]), int(r["site_id"]), r["clinic_name"], r["specialty"]) for r in reader]
        cursor.executemany("INSERT INTO clinics VALUES (?, ?, ?, ?);", rows)
            
    # Load appointments.csv
    with open(csv_files["appointments"], "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        appt_rows = []
        for r in reader:
            appt_rows.append((
                int(r["appointment_id"]),
                int(r["patient_id"]),
                int(r["clinic_id"]),
                r["appointment_date"],
                r["status"],
                float(r["fee"])
            ))
        cursor.executemany("INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?);", appt_rows)
            
    conn.commit()
    
    # Independent reconciliation check comparing raw CSV line counts vs database table counts
    print("=== Independent Database Load Reconciliation Check ===")
    all_ok = True
    for table in ["sites", "clinics", "appointments"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        table_count = cursor.fetchone()[0]
        csv_count = csv_counts[table]
        status = "OK" if table_count == csv_count else "MISMATCH"
        if status != "OK":
            all_ok = False
        print(f"{table}: {csv_count} in CSV, {table_count} in table, {status}")
        
    conn.close()
    if all_ok:
        print(f"Database successfully created and validated at {db_path}")
    else:
        print("Warning: Row count mismatch detected during load validation!")

if __name__ == "__main__":
    load_database()