import json
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"
INPUT = DATA / "appointments_messy.csv"
PLANTED = DATA / "planted_counts.json"
CLEAN_OUT = DATA / "appointments_clean.csv"
REJECTED_OUT = DATA / "rejected_rows.csv"

CLINIC_MAP = {
    "cardio outpatients": "Cardiology",
    "ortho": "Orthopaedics",
    "derm": "Dermatology",
    "cardiology": "Cardiology",
    "orthopaedics": "Orthopaedics",
    "dermatology": "Dermatology",
}
STATUS_MAP = {
    "completed": "Completed",
    "no show": "No-Show",
    "no-show": "No-Show",
    "cancelled": "Cancelled",
}


def count_expected_rows(path):
    """Independent count: non-blank physical lines minus the header."""
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip()) - 1


def load(path):
    """Read everything as text so IDs stay '1234', not 1234.0, and blanks stay ''."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def parse_dates(series):
    """Explicit formats only: UK day-first, then ISO. Anything else (impossible dates) -> NaT."""
    text = series.str.strip()
    uk = pd.to_datetime(text, format="%d/%m/%Y", errors="coerce")
    iso = pd.to_datetime(text, format="%Y-%m-%d", errors="coerce")
    return uk.fillna(iso)


def reject(df, mask, reason):
    """Only label rows that have no reason yet, so each row keeps its FIRST problem."""
    df.loc[mask & (df["reason"] == ""), "reason"] = reason


def main():
    # 1. Expected count (independent of pandas) and raw copy for the rejected file
    expected = count_expected_rows(INPUT)
    df = load(INPUT)
    raw = df.copy()

    # 2. Cleaned columns; unmapped values stay NaN so failures are visible
    df["clinic_clean"] = df["clinic"].str.strip().str.lower().map(CLINIC_MAP)
    df["status_clean"] = df["status"].str.strip().str.lower().map(STATUS_MAP)
    parsed = parse_dates(df["date"])
    fee_text = df["fee"].str.replace("£", "", regex=False).str.strip()
    fee_num = pd.to_numeric(fee_text, errors="coerce")

    # 3. Reasons
    df["reason"] = ""

    # 4. Rejection order matters: it decides the label when a row has several problems
    id_blank = df["appointment_id"].str.strip().eq("")
    date_blank = df["date"].str.strip().eq("")
    date_bad = parsed.isna() & ~date_blank
    fee_blank = fee_text.eq("")

    reject(df, id_blank, "blank_id")
    reject(df, date_blank, "blank_date")
    reject(df, date_bad, "impossible_date")
    reject(df, df["status_clean"].isna(), "unknown_status")
    reject(df, df["clinic_clean"].isna(), "unknown_clinic")
    reject(df, fee_blank, "blank_fee")
    reject(df, fee_num.lt(0), "negative_fee")

    # 5. Duplicates last, only among still-valid rows (first valid copy wins)
    valid = df["reason"].eq("")
    is_dup = (
        df.loc[valid, "appointment_id"].str.strip().duplicated(keep="first")
        .reindex(df.index, fill_value=False)
    )
    reject(df, is_dup, "duplicate_id")

    # 6. Split and write
    bad = df["reason"].ne("")
    rejected = raw[bad].assign(reason=df.loc[bad, "reason"])
    clean = pd.DataFrame({
        "appointment_id": df["appointment_id"].str.strip(),
        "clinic": df["clinic_clean"],
        "date": parsed.dt.strftime("%Y-%m-%d"),
        "status": df["status_clean"],
        "fee": fee_num,
    })[~bad]
    assert clean.notna().all().all(), "clean rows still contain missing values"

    clean.to_csv(CLEAN_OUT, index=False)
    rejected.to_csv(REJECTED_OUT, index=False)

    # 7. Reconcile
    assert expected == len(clean) + len(rejected), (
        f"row count mismatch: expected {expected}, got {len(clean)} + {len(rejected)}"
    )
    print(f"expected {expected} | clean {len(clean)} | rejected {len(rejected)}")

    planted = json.load(open(PLANTED, encoding="utf-8"))
    found = rejected["reason"].value_counts()
    print(f"{'reason':16s} planted found")
    for key, p in planted.items():
        if key == "total_rows":
            continue
        f = int(found.get(key, 0))
        print(f"{key:16s} {p:7d} {f:5d}  {'OK' if p == f else 'MISMATCH'}")


if __name__ == "__main__":
    main()
