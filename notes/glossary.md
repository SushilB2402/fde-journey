# Glossary

## API
* **Definition:** A set of rules that lets one system ask another for information automatically.
* **Hospital Example:** If we built an automatic link, it could request appointment data directly from the booking system through an API.
* **How It Can Fail:** The booking system could reject the request, go offline, or send incomplete fields.

## Webhook
* **Definition:** An automated alert that sends data to another system the instant a specific event occurs.
* **Hospital Example:** If we built an automatic link, the booking system could automatically send a webhook notification whenever a patient cancels or reschedules an appointment.
* **How It Can Fail:** A network hiccup might cause the alert to drop, leaving the receiving file out of sync.

## Master Data
* **Definition:** The official list of core items—like patient IDs, clinic names, and consultant codes—that every system should agree on.
* **Hospital Example:** A single agreed list of clinic names and codes that the booking system and the cardiology spreadsheet would both use. For example, one name for the clinic, not "Cardiology" in one file and "Cardio Outpatients" in another.
* **How It Can Fail:** Different systems or spreadsheets use different names for the same clinic (e.g., "Cardiology" vs. "Cardio Outpatients"), causing automatic matching to fail.
* **Hypothesis to Test:** Inconsistent master data between the booking system export and the cardiology spreadsheet might explain why Priya finds that the two files "never quite match."

## OLTP (Online Transaction Processing)
* **Definition:** Systems built to handle fast, day-to-day operational tasks like entering appointments or checking in patients.
* **Hospital Example:** The booking system, where appointments are recorded and cancelled.
* **How It Can Fail:** System slowdowns or accidental duplicate entries during busy morning clinics can corrupt operational records.

## OLAP (Online Analytical Processing)
* **Definition:** Systems built to summarize and analyze large amounts of historical data for management decision-making.
* **Hospital Example:** The no-show figure Dana gives the director, built from the booking and cardiology data.
* **How It Can Fail:** If the underlying booking data is incomplete or inaccurate, the analytical summaries will lead to incorrect operational decisions.

## ETL (Extract, Transform, Load)
* **Definition:** A process that takes data out of one system, cleans and reformats it, and saves it into another destination.
* **Hospital Example:** As Dana understands it, Priya exports booking data (extract), lines it up with the cardiology spreadsheet by hand (transform), and passes the result to Dana (load).
* **How It Can Fail:** Mistakes in the cleaning or matching steps can introduce errors into the final report figures.

## ELT (Extract, Load, Transform)
* **Definition:** A process where raw data is copied directly into a destination system first, and then cleaned or reformatted later.
* **Hospital Example:** If the team did this, all raw booking records would be exported straight into a shared storage folder first, and matching rules would be applied afterward.
* **How It Can Fail:** If raw data is loaded without validation, messy or duplicate rows can accumulate and confuse staff.

## Data Warehouse
* **Definition:** A central database designed specifically to store organized, historical data for reporting across an entire organization.
* **Hospital Example:** If the hospital built a data warehouse, it could automatically store historical appointment records and attendance outcomes for all outpatient clinics in one place.
* **How It Can Fail:** Scheduled overnight data updates might fail, leaving managers with outdated figures during Monday reviews.

## Data Lake
* **Definition:** A central storage place that holds large amounts of raw files and data in their original formats until needed.
* **Hospital Example:** If the hospital kept raw exports and spreadsheet copies in one shared storage area, that would be a data lake.
* **How It Can Fail:** Without clear oversight, nobody is sure which files are current or who owns them.

## Batch Processing
* **Definition:** Collecting data over a period of time and processing it all together in one go.
* **Hospital Example:** Priya pulls an export whenever leadership asks for a figure, two or three times a month according to Dana, then works out the rate for that request.
* **How It Can Fail:** Figures are only as fresh as the last run, so managers cannot see what happened earlier today or yesterday.

## Streaming Data
* **Definition:** Moving and processing data continuously as each event happens, rather than waiting for a periodic batch.
* **Hospital Example:** If built, clinic attendance counts could update in real time as each patient checks in or misses an appointment. Dana wants an answer in the meeting, not necessarily live data, so streaming is a hypothesis to test.
* **How It Can Fail:** If the network connection drops momentarily, live counts can temporarily fall out of sync.

## Data Pipeline
* **Definition:** The sequence of steps (manual or automated) that moves data smoothly from where it is created to where it is used.
* **Hospital Example:** If built, an automatic flow could take booking records, match them against the cardiology spreadsheet, and update the no-show report.
* **How It Can Fail:** A breakdown at any single step stops the entire flow, preventing updated figures from reaching the report.