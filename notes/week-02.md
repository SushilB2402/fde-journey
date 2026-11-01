# Week 2 journal

- **Goal this week:** Learn customer discovery, clear technical writing, and enterprise data basics, and extend my Python with exceptions, libraries and file handling.

- **What I did:**
  - **2.1 Customer discovery:** Read *The Mom Test* (chapters 1-5, 8 and the cheatsheet), wrote 10 discovery questions, and ran two role-plays with "Dana", a hospital operations manager. Wrote a one-page discovery summary that separates verified facts from assumptions.
  - **2.2 Technical writing:** Completed Google's Technical Writing One course, wrote a six-rule writing card, and drafted a follow-up email to Dana.
  - **2.3 Enterprise data:** Wrote data fundamentals notes and a plain-English glossary, drew a data-flow diagram, built a failure-point table with detection methods, and scored 5/5 on the self-test.
  - **2.4 Python part 2:** Did the CS50P exception, library and file problems, then wrote `clean_csv.py`, which cleans a messy appointments file and reconciles the row counts.

- **What blocked me:**
  - **Role-play 1:** I pitched the dashboard too early and missed Dana's comment that the report was late. In role-play 2, I stated a success metric without asking her to confirm it, and ended with no concrete commitment from her.
  - **Status email:** The first draft had the wrong date (2 November is a Monday, not a Thursday) and described the matching process as "monthly", which Dana never said.
  - **Blank line:** `csv.DictReader` silently skipped the blank line in my sample file, so my reconciliation check could never fail. It compared two numbers that were always equal.
  - **Mapping regression:** When I rewrote the clinic mapping, I dropped the variants ("Ortho", "Derm", "Cardio Outpatients"). Clean rows fell from 10 to 3, which was the clue that something was wrong.
  - **Git and setup:** My generated CSV files stayed tracked after I added them to `.gitignore`, so I used `git rm --cached`. `tabulate` was installed outside my virtual environment and missing from `requirements.txt`. A pasted command also created a stray empty file, and I once forgot `-m` on `git commit`.

- **What I learned:**
  - Label what Dana said (verified), what she repeated second-hand, and what I assumed. Don't invent facts in examples either.
  - A check that compares a number to itself proves nothing. Count the expected rows independently, from the source.
  - After every change, compare the output counts with what I expected. The 10-to-3 drop caught the mapping mistake.
  - `.gitignore` only affects files Git isn't tracking yet. Record dependencies in `requirements.txt` and work inside the virtual environment.
  - Ask for a concrete next step (a time, a person, some access), not a polite "send it over".

- **Next step:** Close the two open spoken checkpoints (the 2-minute role explanation and three failure points with detection), then start Week 3: SQL, pandas, a Git branch and pull-request workflow, and command-line basics.
