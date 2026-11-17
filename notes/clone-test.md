# Clone test: week 3 pandas cleaning (checkpoint 3.2)

Date: 2026-11-16

**Goal:** prove the pandas cleaning work runs from a fresh clone of GitHub, with nothing depending on files that only exist on my laptop.

**Result: passed.** A fresh clone built its own environment, generated the messy data and reproduced the expected counts.

## What I checked before cloning

- The cleaning work was pushed and merged into `main` on GitHub.
- `git ls-tree -r origin/main --name-only | grep week3/pandas` listed `clean_data.py`, `cleaning_log.md`, `explore.py`, `make_messy_data.py` and `practice.py`.
- The generated `data/` folder is ignored by Git, so the clone starts without data and must create it.

## Steps I ran

```bash
cd ~
deactivate
hash -r
gh repo clone SushilB2402/fde-journey pandas-check
cd pandas-check
python.exe -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python.exe week3/pandas/make_messy_data.py
python.exe week3/pandas/clean_data.py
```

## Output

```
expected 300 | clean 205 | rejected 95
reason           planted found
blank_id              12    12  OK
duplicate_id          15    15  OK
impossible_date       10    10  OK
blank_date             8     8  OK
unknown_status        18    18  OK
unknown_clinic        14    14  OK
negative_fee           8     8  OK
blank_fee             10    10  OK
```

`pip install -r requirements.txt` installed pandas 3.1.1 and numpy 2.5.4 without errors, so `requirements.txt` is complete for these scripts.

## What went wrong on the first attempts

| Problem | Cause | Fix |
|---|---|---|
| The clone had no `week3/pandas` scripts | The pull request had not been pushed and merged yet | Push and merge first, then clone |
| `~/Desktop` did not exist | I assumed a folder that was not there | Clone from `~` and run `pwd` first |
| Every `python` command failed with "No such file or directory" | Bash had a stale cached path to a deleted old clone, and an old `.venv` was still active | `deactivate`, then `hash -r`, then use `python.exe` |

## Lessons

- Run the clone test only after merging, from a folder outside the repo, and check `pwd` before cloning and before deleting.
- A fresh clone is the real test of a project: it exposes missing files and missing packages.
- `hash -r` clears Bash's cached command locations. `deactivate` leaves an old virtual environment.

## Cleanup

```bash
cd ~
pwd                  # must print /c/Users/Sushil Bhosale
rm -r pandas-check
```

- [x] `pandas-check` deleted (tick once `ls ~` no longer lists it)
