import pytest
from clean_csv import parse_date, field, clean_row

def test_parse_date_valid():
    dt = parse_date("25/12/2026")
    assert dt.year == 2026
    assert dt.month == 12
    assert dt.day == 25

def test_parse_date_invalid_format():
    with pytest.raises(ValueError, match="Invalid date"):
        parse_date("2026-12-25")

def test_parse_date_impossible_date():
    with pytest.raises(ValueError, match="Invalid date"):
        parse_date("31/02/2026")

def test_field_safe_retrieval():
    row = {"appointment_id": "APT101", "clinic": None}
    assert field(row, "appointment_id") == "APT101"
    assert field(row, "clinic") == ""
    assert field(row, "missing_col") == ""

def test_clean_row_valid():
    row = {
        "appointment_id": "APT201",
        "clinic": "cardio outpatients",
        "date": "15/05/2026",
        "status": "ATTENDED"
    }
    seen = set()
    cleaned = clean_row(row, seen)
    assert cleaned["appointment_id"] == "APT201"
    assert cleaned["clinic"] == "Cardiology"
    assert cleaned["status"] == "attended"

def test_clean_row_missing_id():
    row = {"appointment_id": "", "clinic": "Cardiology", "date": "15/05/2026", "status": "attended"}
    with pytest.raises(ValueError, match="Missing appointment_id"):
        clean_row(row, set())

def test_clean_row_duplicate_id():
    row = {"appointment_id": "APT101", "clinic": "Cardiology", "date": "15/05/2026", "status": "attended"}
    seen = {"APT101"}
    with pytest.raises(ValueError, match="Duplicate appointment_id"):
        clean_row(row, seen)

def test_clean_row_invalid_status():
    row = {"appointment_id": "APT202", "clinic": "Cardiology", "date": "15/05/2026", "status": "maybe"}
    with pytest.raises(ValueError, match="Invalid status"):
        clean_row(row, seen_ids=set())

def test_clean_row_too_many_columns():
    # DictReader places unkeyed extra columns under key `None`
    row = {"appointment_id": "APT203", "clinic": "Cardiology", "date": "15/05/2026", "status": "attended", None: "ExtraData"}
    with pytest.raises(ValueError, match="Too many columns"):
        clean_row(row, seen_ids=set())