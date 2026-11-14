import pandas as pd

print("=== INITIAL RAW DATAFRAME (6 ROWS) ===")
raw = pd.DataFrame({
    "appointment_id": [1, 2, 2, None, 5, 6],
    "clinic": ["Cardiology", " cardio outpatients", "Ortho", "Derm", None, "Unknown Clinic"],
    "date": ["01/03/2026", "31/02/2026", "2026-03-04", "05/03/2026", "", "15/03/2026"],
    "status": ["Completed", "no show", "No-Show", "Cancelled", "completed", "Pending"],
    "fee": ["£120.50", "130", "-15.00", "", "£80", "200"],
})
print(raw)
print("\n" + "=" * 60 + "\n")

# ==============================================================================
# DRILL 1: Missing values (isolated test on raw.copy())
# ==============================================================================
print("--- Drill 1: Missing Values ---")
df = raw.copy()
print("Before replace('', pd.NA):")
print(df.isna().sum())

empty_cells = (df == "").sum().sum()
df = df.replace("", pd.NA)
print(f"\nCells converted from '' to pd.NA: {empty_cells}")
print("After replace('', pd.NA):")
print(df.isna().sum())
print("\n" + "=" * 60 + "\n")

# ==============================================================================
# DRILL 2: Duplicates & Missing IDs (isolated test on raw.copy())
# ==============================================================================
print("--- Drill 2: Duplicates & Missing IDs ---")
df = raw.copy().replace("", pd.NA)

missing_id_count = df["appointment_id"].isna().sum()
print(f"Rows with missing appointment_id: {missing_id_count}")

dups = df[df["appointment_id"].notna() & df.duplicated(subset=["appointment_id"], keep=False)]
print(f"Rows sharing a non-null appointment_id: {len(dups)}")
print(dups)

before_rows = len(df)
df = df.dropna(subset=["appointment_id"])
df = df.drop_duplicates(subset=["appointment_id"], keep="first")
after_rows = len(df)
print(f"Rows dropped (missing ID + duplicates): {before_rows - after_rows} (before: {before_rows}, after: {after_rows})")
print("\n" + "=" * 60 + "\n")

# ==============================================================================
# DRILL 3: Types & Fee Cleaning (isolated test on raw.copy())
# ==============================================================================
print("--- Drill 3: Types & Fee Cleaning ---")
df = raw.copy().replace("", pd.NA)
before_na_fees = df["fee"].isna().sum()

# Clean string values without turning actual NA into "nan"/"None"
fee_cleaned = df["fee"].where(df["fee"].isna(), df["fee"].astype(str).str.replace("£", "", regex=False).str.strip())
df["fee"] = pd.to_numeric(fee_cleaned, errors="coerce")

after_na_fees = df["fee"].isna().sum()
neg_fees = (df["fee"] < 0).sum()
print(f"Missing fees before coercion: {before_na_fees}, after coercion: {after_na_fees} (newly coerced NaNs: {after_na_fees - before_na_fees})")
print(f"Negative fees detected: {neg_fees}")
print(df[["appointment_id", "fee"]])
print("\n" + "=" * 60 + "\n")

# ==============================================================================
# DRILL 4: Explicit Date Parsing (isolated test on raw.copy())
# ==============================================================================
print("--- Drill 4: Explicit Date Parsing ---")
df = raw.copy().replace("", pd.NA)
raw_dates = df["date"].copy()

d_uk = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
d_iso = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
df["date"] = d_uk.fillna(d_iso)

print(f"Total NaT dates after parsing: {df['date'].isna().sum()} (from {raw_dates.isna().sum()} blank + {df['date'].isna().sum() - raw_dates.isna().sum()} invalid date strings)")
print("\nRaw date vs Parsed date:")
print(pd.DataFrame({"raw_date": raw_dates, "parsed_date": df["date"]}))
print("\n" + "=" * 60 + "\n")

# ==============================================================================
# DRILL 5: Text Standardisation & Master-Data Mapping (isolated test on raw.copy())
# ==============================================================================
print("--- Drill 5: Text Standardisation & Mapping ---")
df = raw.copy().replace("", pd.NA)

# Preserve actual missing values before string operations
clinic_norm = df["clinic"].where(df["clinic"].isna(), df["clinic"].astype(str).str.strip().str.lower())
status_norm = df["status"].where(df["status"].isna(), df["status"].astype(str).str.strip().str.lower())

clinic_map = {
    "cardiology": "Cardiology",
    "cardio outpatients": "Cardiology",
    "ortho": "Orthopaedics",
    "orthopaedics": "Orthopaedics",
    "derm": "Dermatology",
    "dermatology": "Dermatology",
}

status_map = {
    "completed": "Completed",
    "no show": "No-Show",
    "no-show": "No-Show",
    "cancelled": "Cancelled",
}

mapped_clinic = clinic_norm.map(clinic_map)
unmapped_clinics = df["clinic"][mapped_clinic.isna()].tolist()
print(f"Unmapped/missing clinic entries becoming NaN ({len(unmapped_clinics)}): {unmapped_clinics}")

mapped_status = status_norm.map(status_map)
unmapped_statuses = df["status"][mapped_status.isna()].tolist()
print(f"Unmapped/missing status entries becoming NaN ({len(unmapped_statuses)}): {unmapped_statuses}")

df["clinic"] = mapped_clinic
df["status"] = mapped_status
print("\nAfter mapping:")
print(df[["appointment_id", "clinic", "status"]])
print("\n" + "=" * 60 + "\n")

# ==============================================================================
# DRILL 6: Full Ordered Pipeline & Validation Asserts
# ==============================================================================
print("--- Drill 6: Full Ordered Pipeline & Validation ---")
df = raw.copy()
start_count = len(df)
print(f"Starting row count: {start_count}")

# 1. Convert empty strings to pd.NA
df = df.replace("", pd.NA)

# 2. Parse dates explicitly (before dropping rows so all formats are tested)
d_uk = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
d_iso = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
df["date"] = d_uk.fillna(d_iso)

# 3. Clean fees
fee_str = df["fee"].where(df["fee"].isna(), df["fee"].astype(str).str.replace("£", "", regex=False).str.strip())
df["fee"] = pd.to_numeric(fee_str, errors="coerce")

# 4. Standardise and map text fields
clinic_clean = df["clinic"].where(df["clinic"].isna(), df["clinic"].astype(str).str.strip().str.lower())
status_clean = df["status"].where(df["status"].isna(), df["status"].astype(str).str.strip().str.lower())
df["clinic"] = clinic_clean.map(clinic_map)
df["status"] = status_clean.map(status_map)

# 5. Reject rows violating hard business rules
# - Reject missing appointment_id
before = len(df)
df = df.dropna(subset=["appointment_id"])
print(f"Dropped rows with missing appointment_id: {before - len(df)}")

# - Reject duplicate appointment_id
before = len(df)
df = df.drop_duplicates(subset=["appointment_id"], keep="first")
print(f"Dropped duplicate appointment_id rows: {before - len(df)}")

# - Reject invalid/NaT dates, unmapped statuses, or negative/missing fees
before = len(df)
df = df[
    df["date"].notna()
    & df["status"].notna()
    & df["fee"].notna()
    & (df["fee"] >= 0)
].copy()
print(f"Dropped rows with invalid dates, unmapped status, or bad fees: {before - len(df)}")
print(f"Final clean row count: {len(df)} (total dropped: {start_count - len(df)})")

print("\nFinal Cleaned DataFrame:")
print(df)

# Four validation asserts
assert df["appointment_id"].notna().all(), "Missing appointment_id found!"
assert df["appointment_id"].duplicated().sum() == 0, "Duplicate appointment_id found!"
print("✓ Assert 1 passed: All appointment_ids are present and unique.")

allowed_statuses = {"Completed", "No-Show", "Cancelled"}
assert df["status"].isin(allowed_statuses).all(), "Invalid status found!"
print("✓ Assert 2 passed: Every status is in the allowed set.")

start_date = pd.Timestamp("2026-01-01")
end_date = pd.Timestamp("2026-04-01")
assert df["date"].between(start_date, end_date).all(), "Dates out of range (1 Jan to 1 Apr 2026)!"
print("✓ Assert 3 passed: All dates are within 1 Jan to 1 Apr 2026.")

assert (df["fee"] >= 0).all(), "Negative fee found!"
print("✓ Assert 4 passed: All fees are >= 0.")

print("\nAll 6 drills and validation checks passed!")