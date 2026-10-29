# Discovery Summary: Outpatient No-Show Reporting & Clinic Reconciliation

## 1. Problem Statement
Leadership review meetings (such as the Monday operations meeting) require immediate, accurate no-show metrics across outpatient clinics. Currently, retrieving these figures takes up to 48 hours because reporting requires manual exports from the booking system and manual cross-referencing against clinic-specific spreadsheets. This delay prevents timely operational decisions—such as extending pilot programs—and forces critical items to be parked for a month.

## 2. Users & Stakeholders
* **Dana (Operations Manager, Outpatient Services):** Primary user and decision-maker for operational pilots and clinic workflows; accountable to executive leadership for clinic metrics.
* **Priya (Reporting / Data Role):** The individual responsible for pulling system exports and manually reconciling data against spreadsheets.
* **Clinic Leadership / Director:** Executive stakeholders who consume the metrics during weekly/monthly reviews to make scaling decisions (e.g., text-message reminder pilots).
* **Cardiology Clinic Staff:** The team currently maintaining separate tracking spreadsheets for their clinic.

## 3. Constraints
* **Time & Capacity:** Dana has extremely limited time between clinics (30-minute meeting windows), and Priya is already stretched thin.
* **Data Access & Compliance:** Any technical solution must comply with internal data governance policies regarding the use of booking system exports.
* **Risk Tolerance:** Incorrect or untrusted figures presented to the director directly impact operational credibility.

## 4. Success Metric (Proposed & Unconfirmed)
* **Definition:** During the Monday leadership meeting, Dana is able to instantly provide a trusted, accurate no-show rate for any outpatient clinic upon request, eliminating the "I'll get back to you by Wednesday" delay and preventing decisions from being parked. 
* **Validation Status:** *Proposed based on Dana's input, but requires formal confirmation regarding exact response time thresholds and specific trust criteria.*

## 5. Open Questions
* How do other clinics (outside of cardiology) currently track their no-show data? Do they also rely on separate spreadsheets?
* What specific discrepancies cause booking system exports and clinic spreadsheets to misalign?
* Who in IT or compliance must approve data access before a prototype can be tested against live records?

---

## Verified Facts vs. Unverified Assumptions

### Verified Facts (Directly Stated by Dana)
* A recent request for cardiology no-show rates took nearly 48 hours to fulfill (asked Monday, delivered Wednesday).
* The data required Priya to pull a booking system export and manually reconcile it with a separate cardiology spreadsheet.
* The delay caused a decision on extending the text-message reminder pilot (which sat at a 14% no-show rate) to be parked for an entire month, resulting in continued empty clinic slots.
* Ad-hoc reporting requests occur roughly 2 to 3 times a month, increasing during budget season or clinic complaints.
* Dana wants the ability to answer leadership inquiries live during Monday meetings without needing a multi-day turnaround.
* Priya reports that the two data sources "never quite match," though the root cause is unverified.
* Dana expressed caution about premature prototypes to protect her standing with the director and verify data permissions.

### Unverified Assumptions
* **The Solution Shape:** Assumes a dashboard is the optimal fix; a scheduled automated report or a streamlined reconciliation view might solve the problem with less friction.
* **Data Discrepancy Causes:** Assumes the mismatch between booking exports and cardiology spreadsheets is due to human entry error or timing offsets, rather than systemic sync issues.
* **Cross-Clinic Uniformity:** Assumes other outpatient clinics maintain separate tracking spreadsheets similar to cardiology.
* **Technical Feasibility:** Assumes direct automated integration between the booking system and clinic spreadsheets is permitted under current IT compliance policies.