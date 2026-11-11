# Healthcare SQL Practice Pipeline

## Purpose
A lightweight SQLite and Python data pipeline built for operational analytics, relational modeling, and SQL query practice. All data is fictional.

## Project Structure & File Manifest
```text
week3/sql-practice/
│
├── data/                  # CSV source data files (generated, not committed)
│   ├── sites.csv
│   ├── clinics.csv
│   └── appointments.csv
│
├── make_data.py           # Python script to generate synthetic CSV data (~1000 appointments)
├── load_db.py             # ETL script to initialize schema, enforce FKs, load DB, and run reconciliation
├── healthcare.db          # SQLite database instance (generated, not committed)
├── queries.sql            # Operational and analytical SQL queries
└── README.md              # Project documentation