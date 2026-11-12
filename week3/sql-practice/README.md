# Healthcare SQL Practice Project

A small SQLite and Python project for practising SQL on a made-up outpatient appointments database. **All data is fictional.** No real patient, clinic or hospital data is used.

The project asks one question: which clinics have a high no-show rate, and does the answer change depending on how you slice the data?

## Project structure

```text
week3/sql-practice/
├── make_data.py     generates the CSV files (fixed seed, so the data is reproducible)
├── load_db.py       builds the SQLite database and checks the row counts
├── queries.sql      13 queries, with the rules they follow written at the top
├── README.md        this file
├── data/            generated CSV files (not committed)
│   ├── sites.csv
│   ├── clinics.csv
│   └── appointments.csv
└── healthcare.db    generated database (not committed)
```

`data/` and `healthcare.db` are created by the scripts and are listed in `.gitignore`.

## How to run

Only Python's standard library is needed (`csv`, `random`, `sqlite3`). Run these from the repository root:

```text
python week3/sql-practice/make_data.py
python week3/sql-practice/load_db.py
```

`load_db.py` prints a row-count check for each table, and every line should end in `OK`. Then open `healthcare.db` in any SQLite tool and run the queries in `queries.sql`.

## Data model

| Table | Columns | Notes |
|---|---|---|
| `sites` | `site_id`, `site_name`, `region` | 3 sites in 3 regions |
| `clinics` | `clinic_id`, `site_id`, `clinic_name`, `specialty` | 6 clinics, one of which has no appointments |
| `appointments` | `appointment_id`, `patient_id`, `clinic_id`, `appointment_date`, `status`, `fee` | 1,000 rows from 1 Jan to 1 Apr 2026 |

Relationships: `appointments.clinic_id` points to `clinics.clinic_id`, and `clinics.site_id` points to `sites.site_id`. Foreign keys are enforced during the load. `status` is `Completed`, `No-Show` or `Cancelled`.

## Definitions

- **Revenue:** only appointments with status `Completed` count. Fees on no-shows and cancellations are ignored.
- **No-show rate:** no-shows divided by all appointments, including cancelled ones.
- **Overall average (Q13):** the pooled rate (total no-shows divided by total appointments), not the average of the clinic rates.
- **Partial April:** the data ends on 1 April, so Q8 and Q11 exclude April. Their monthly totals add up to slightly less than the full table.

## Queries

| Queries | Topic |
|---|---|
| 1, 2, 9 | Listing clinics, counting appointments, and finding the clinic with none (LEFT JOIN) |
| 3, 4, 5 | Status mix, completed revenue per clinic, clinics above a 20% no-show rate (HAVING) |
| 6, 7, 8, 10 | Revenue by region, by patient, by month, and by site and clinic |
| 11, 12, 13 | No-show rate by month, by region (a three-table join), and for clinics above the system average (a subquery) |

## Self-checks

- The loader's row counts match the CSV files.
- The completed counts in Q4 add up to the Completed total in Q3.
- The appointment counts in Q12 add up to the number of rows in `appointments`.
- Q9 returns the empty clinic.

## Limits and notes

- **The clinic differences are designed, not discovered.** `make_data.py` sets a no-show rate for each clinic (10%, 25%, 5%, 35% and 20%), so the data shows what it was built to show.
- **Rates are noisy.** Each clinic has about 200 appointments, so a rate can move by a few points between runs of a different seed. A clinic set at exactly 20% can fall on either side of a 20% threshold by chance.
- **A regional rate can hide a clinic.** All three regions come out at a similar rate, but one clinic inside a region is much worse. Q12 shows the region view and Q5 shows the clinic view.
- **One partial month.** April has only one day of data.
