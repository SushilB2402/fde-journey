import csv
from datetime import datetime
from pathlib import Path
import json
from collections import Counter

# Master data mapping restoring clinic variants (keys in Title Case to match .title())
CLINIC_MAPPING = {
    "Cardiology": "Cardiology",
    "Cardio Outpatients": "Cardiology",
    "Ortho": "Orthopaedics",
    "Orthopaedics": "Orthopaedics",
    "Derm": "Dermatology",
    "Dermatology": "Dermatology"
}

VALID_STATUSES = {"attended", "no-show"}

def field(row, name):
    """Safely retrieves and strips a field value, handling missing columns (None)."""
    return (row.get(name) or "").strip()

def parse_date(date_str):
    """Parses and validates date string. 
    Note: Returns the parsed datetime object for format/validity checks, 
    even though the raw string is retained for output.
    """
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt
    except ValueError:
        raise ValueError(f"Invalid date: '{date_str}'")

def clean_row(row, seen_ids):
    """Validates and cleans a single row. Raises ValueError if validation fails."""
    if None in row:
        raise ValueError("Too many columns")

    # 1. Check for missing appointment_id
    app_id = field(row, "appointment_id")
    if not app_id:
        raise ValueError("Missing appointment_id")

    # 2. Check for duplicate appointment_id within the file
    if app_id in seen_ids:
        raise ValueError(f"Duplicate appointment_id: {app_id}")

    # 3. Validate date format and existence
    date_raw = field(row, "date")
    if not date_raw:
        raise ValueError("Missing date")
    parse_date(date_raw)

    # 4. Validate status
    status = field(row, "status").lower()
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: '{status}'")

    # 5. Normalize clinic name case-insensitively using master data variants
    clinic_raw = field(row, "clinic")
    if not clinic_raw:
        raise ValueError("Missing clinic")
    
    normalized_key = clinic_raw.title()
    if normalized_key not in CLINIC_MAPPING:
        raise ValueError(f"Unknown clinic name: '{clinic_raw}'")
    
    normalized_clinic = CLINIC_MAPPING[normalized_key]

    return {
        "appointment_id": app_id,
        "clinic": normalized_clinic,
        "date": date_raw,
        "status": status
    }

def main():
    script_dir = Path(__file__).parent
    input_file = script_dir / "sample_appointments.csv"
    clean_output = script_dir / "clean_appointments.csv"
    rejected_output = script_dir / "rejected_rows.csv"
    summary_output = script_dir / "rejection_summary.json"

    if not input_file.exists():
        print(f"Error: The input file '{input_file.name}' was not found in '{script_dir}'.")
        return

    # Count lines independently for reconciliation
    with open(input_file, encoding="utf-8") as f:
        total_lines = sum(1 for _ in f)
    with open(input_file, encoding="utf-8") as f:
        non_empty = sum(1 for line in f if line.strip())
    
    blank_lines = total_lines - non_empty
    
    # Handle empty or header-only files safely using max()
    expected_rows = max(non_empty - 1, 0)
    if expected_rows == 0 and total_lines <= 1:
        print("File is empty or contains only a header. Stopping processing.")
        return

    clean_rows = []
    rejected_rows = []
    seen_ids = set()

    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        
        for raw_row in reader:
            # Note: Edge case — a line containing only whitespace is skipped by 
            # non_empty line counting but may be parsed as an empty row by DictReader,
            # causing a slight reconciliation delta if present.
            try:
                cleaned = clean_row(raw_row, seen_ids)
                seen_ids.add(cleaned["appointment_id"])
                clean_rows.append(cleaned)
            
            except ValueError as e:
                rejected_row = {
                    "appointment_id": field(raw_row, "appointment_id"),
                    "clinic": field(raw_row, "clinic"),
                    "date": field(raw_row, "date"),
                    "status": field(raw_row, "status"),
                    "reason": str(e)
                }
                rejected_rows.append(rejected_row)

    # Write clean rows output
    with open(clean_output, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["appointment_id", "clinic", "date", "status"])
        writer.writeheader()
        writer.writerows(clean_rows)

    # Write rejected rows output with reason column
    with open(rejected_output, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["appointment_id", "clinic", "date", "status", "reason"])
        writer.writeheader()
        writer.writerows(rejected_rows)

    # Group rejection reasons by category prefix for meaningful summary metrics
    reason_categories = [row["reason"].split(":")[0] for row in rejected_rows]
    reason_counts = Counter(reason_categories)

    total_processed = len(clean_rows) + len(rejected_rows)
    reconciliation_match = (expected_rows == total_processed)

    summary_data = {
        "total_file_lines": total_lines,
        "blank_lines_skipped": blank_lines,
        "expected_data_rows": expected_rows,
        "clean_rows_written": len(clean_rows),
        "rejected_rows_written": len(rejected_rows),
        "reconciliation_match": reconciliation_match,
        "rejection_categories": dict(reason_counts)
    }

    with open(summary_output, mode="w", encoding="utf-8") as jsonfile:
        json.dump(summary_data, jsonfile, indent=4)

    # Print explicit reconciliation equation and metrics report
    print("==========================================")
    print("          RECONCILIATION REPORT           ")
    print("==========================================")
    print(f"Total File Lines:     {total_lines}")
    print(f"Blank Lines Skipped:  {blank_lines}")
    print(f"Expected Data Rows:   {expected_rows}")
    print(f"Clean Rows Written:   {len(clean_rows)}")
    print(f"Rejected Rows Written:{len(rejected_rows)}")
    print(f"Summary Exported to:  {summary_output.name}")
    print(f"Reconciliation Check: {expected_rows} = {len(clean_rows)} + {len(rejected_rows)} "
          f"({'MATCH' if reconciliation_match else 'MISMATCH'})")
    print("==========================================")

if __name__ == "__main__":
    main()