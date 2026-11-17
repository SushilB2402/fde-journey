# FDE Journey

My learning log for the forward deployed engineer path: weekly notes, exercises and small projects. **All data is fictional.** No real patient, clinic or hospital data is used.

## Progress

| Week | Focus | Status | Notes |
| --- | --- | --- | --- |
| 1 | The FDE role, development setup (VS Code, Python 3.13, Git), CS50P lectures 0 to 2 | Done | [notes/week-01.md](notes/week-01.md) |
| 2 | Customer discovery, technical writing, enterprise data, Python part 2 | Done, except two spoken checkpoints | [notes/week-02.md](notes/week-02.md) |
| 3 | SQL, pandas data cleaning, Git workflow, command line | Done | [notes/week-03.md](notes/week-03.md) |

## Projects

| Project | What it shows | How to run (from the repository root) |
| --- | --- | --- |
| [SQL practice](week3/sql-practice/README.md) | A SQLite and Python project on a made-up appointments database, with 13 queries on no-show rates | `python week3/sql-practice/make_data.py` then `python week3/sql-practice/load_db.py` |
| Pandas cleaning (`week3/pandas`) | A messy-data generator and a cleaner that rejects bad rows with a reason and reconciles the counts: 300 rows in, 205 clean, 95 rejected | `python week3/pandas/make_messy_data.py` then `python week3/pandas/clean_data.py` |
| Shell scripts (`week3/shell`) | `organise_files.sh` renames and archives a folder, and `log_search.md` finds and counts errors in a large log with one pipeline | `bash week3/shell/organise_files.sh <folder>` |

Generated files (`data/` folders, databases, the shell sandbox) are created by the scripts and are listed in `.gitignore`, so they are not committed.

## Setup

```text
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

These commands are for Git Bash on Windows with Python 3.13. The SQL project needs only Python's standard library, and the pandas project uses the packages in `requirements.txt`.

## How I work

- Every change goes on a branch and through a pull request, following [notes/git-workflow.md](notes/git-workflow.md).
- Labs and experiments run in a folder outside this repository.
- The pandas project was checked from a fresh clone ([notes/clone-test.md](notes/clone-test.md)).
