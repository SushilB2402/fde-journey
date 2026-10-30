# Failure-Point Analysis: Outpatient No-Show Reporting

This document analyzes operational and data failure points, their impact, verification status, and methods for detection.

| # | Failure Point | What Goes Wrong | Status | How You Would Detect It |
|---|---|---|---|---|
| **1** | **Matching** | The two files "never quite match" | Reported by Dana (second-hand) | Row counts: check if `source rows = matched + unmatched`; review the unmatched list. |
| **2** | **Turnaround** | The figure arrives Wednesday, after the Monday meeting | Verified (last request) | Log request date and delivery date; show a prominent "data as of" timestamp on the report. |
| **3** | **One person knows the steps** | Dana doesn’t know the matching steps; Priya is the person to ask. If Priya is away, nobody may know them. | Likely (Dana: “Priya’s the person to ask”) | Test if anyone else can run the matching process using written documentation alone. |
| **4** | **Timing Discrepancies** | The booking export and cardiology spreadsheet are extracted at different times | Hypothesis | Record an "as of" timestamp on both source files and compare the latest date/time stamps. |
| **5** | **Manual Entry Errors** | Typing or formatting errors exist within the cardiology spreadsheet | Hypothesis | Run automated checks for duplicate IDs and impossible dates; perform periodic second-person spot checks. |
| **6** | **Data-use rules / Access** | Booking system data may not be permitted in an external or prototype tool | Unknown (Dana to check) | Ask IT or compliance to confirm the data-use rules in writing. Until they do, test with made-up sample data only, not real records. |