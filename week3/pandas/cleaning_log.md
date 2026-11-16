# Week 3 Data Cleaning Audit Log (`week3/pandas/`)


# Cleaning log: appointments_messy.csv

## 1. Pipeline Overview & Row Conservation
- **Input Source:** `data/appointments_messy.csv`
- **Total Non-Empty Physical Records:** $300$ (verified independently via line inspection excluding header and intentional blank lines)
- **Clean Output (`data/appointments_clean.csv`):** $205$ rows
- **Rejected Output (`data/rejected_rows.csv`):** $95$ rows
- **Conservation Check:** $205 + 95 = 300$ rows ($100\%$ accounted for; zero silent drops)


Input: 300 rows. Output: 205 clean, 95 rejected (every row accounted for).

| Problem | Planted | Found | Decision | Why |
|---|---|---|---|---|
| Blank ID | 12 | 12 | Reject | A row with no ID cannot be identified |
| Blank date | 8 | 8 | Reject | Without a date it cannot be reported or scheduled |
| Impossible date | 10 | 10 | Reject | The date does not exist (e.g. 31/04/2026); guessing would invent data |
| Unknown status | 18 | 18 | Reject | "Pending" is not a status the reports understand |
| Unknown clinic | 14 | 14 | Reject | "Unknown Clinic" cannot be assigned to a department |
| Blank fee | 10 | 10 | Reject | Not recorded; filling in 0 or an average would distort revenue |
| Negative fee | 8 | 8 | Reject | A fee cannot be negative; may be a refund, so ask the client |
| Duplicate ID | 15 | 15 | Reject extra copies, keep first valid | The same appointment must be counted once |

## 2. Noise fixed (rows kept)
- Stray spaces trimmed: 142 cells (75 clinic, 67 status)
- £ signs stripped from fees: 146
- ISO dates (YYYY-MM-DD) parsed alongside DD/MM/YYYY: 132
- Clinic variants mapped to standard names: 71 (cardio outpatients, ortho, derm)
- Status variants mapped to standard names: 88 (no show, no-show, cancelled and similar)

## 3. Assumptions
- Dates are day first (UK), e.g. 01/03/2026 is 1 March.
- A blank fee is rejected, not treated as zero.
- The first valid copy of a duplicate ID is kept.
- Each row gets the first problem found, in this order: blank ID, blank date, impossible date, unknown status, unknown clinic, blank fee, negative fee, duplicate ID.
- All data is fictional.