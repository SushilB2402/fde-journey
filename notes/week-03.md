# Week 3 Journal

- **Goal this week:** Learn SQL, pandas data cleaning, a Git branch and pull-request workflow, and command-line basics.

- **What I did:**
  - **3.1 SQL:** Finished SQLBolt (lessons 1-12), the SQLZoo joins and aggregates, and an appointments database project with 13 queries (PRs #4 and #5). The timed three-table join took 8 min 28 s.
  - **3.2 pandas:** Wrote `explore.py`, which matches my SQL results, then a messy-data generator and `clean_data.py`. The cleaner reads 300 rows, writes 205 clean and 95 rejected rows with a reason for each, and the planted counts equal the found counts for all 8 problems. I wrote a cleaning log, and a fresh-clone test reproduced the same counts (PRs #6, #7, #9, #10, #11).
  - **3.3 Git workflow:** Ran the branch, pull request and merge loop for every change. Wrote `notes/git-workflow.md` (PRs #12, #14, #15) and resolved two merge conflicts. The second one I resolved from memory in a scratch folder (merge commit `1d2fe25`).
  - **3.4 Command line:** Did the ten shell practice tasks, wrote `organise_files.sh` (renames and archives a folder), and searched a 5,023-line log with one pipeline (PR #16).

- **What blocked me:**
  - **Generator counts:** The cleaner found 13 blank IDs instead of the 12 I planted. A duplicate had copied a row whose ID was already blank. I fixed it by reserving clean source rows for the duplicates.
  - **Log pipeline:** `uniq -c` showed 1 for every line, because timestamps, services and numbers made every line different. I cut those fields out first.
  - **Script:** My first `organise_files.sh` added the date prefix twice on a second run and wrote the archive outside the ignored sandbox.
  - **Git slips:** I committed on `main` by accident, pushed an empty branch, ran the conflict lab inside my real repo, ran the clone test before the merge, and lost the code fence around the conflict example in my notes.
  - **Command blocks:** I pasted whole command blocks at once, so verify and cleanup ran before the work they checked. Edit first, check `git status -sb` for `M`, then run the chain.

- **What I learned:**
  - Count the expected rows independently, and compare planted with found. A mismatch means a bug in the data or in the checker.
  - Chain Git commands with `&&`, check `git branch --show-current` before committing, and run labs in a folder outside the repo.
  - `uniq -c` only groups identical lines, so strip the varying parts first.
  - A fresh clone is the real test of whether a project runs.
  - Check `pwd` before every `rm`.

- **Next step:** Record the two open Week 2 spoken checkpoints, delete the leftover branches, then start Week 4.
