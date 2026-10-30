# Data Fundamentals: Notes from Microsoft Learn (Azure Data Fundamentals)

Concept notes for task 2.3, tied to the hospital no-show reporting project. Check each section against the Microsoft Learn modules before relying on it.

---

## 1. Core data concepts

### Data types
| Type | What it is | Example |
|---|---|---|
| Structured | Rows and columns with a fixed layout; stored in relational databases | Customers, Orders and Products tables |
| Semi-structured | Flexible layout with labelled fields; JSON and XML | See the JSON below |
| Unstructured | No fixed layout | Images, videos, PDFs, audio files |

```json
{
  "customerId": 1001,
  "name": "Alex",
  "city": "Leeds"
}
```

### Transactional (OLTP) vs analytical (OLAP) workloads
| | Transactional (OLTP) | Analytical (OLAP) |
|---|---|---|
| Purpose | Run day-to-day operations | Reporting and decision-making |
| Examples | Banking transactions, online orders, airline bookings | Sales trends, customer behaviour, executive reports |
| Typical work | Many small updates, fast responses | Large queries, mostly reading |
| Data | Current | Historical |

In practice: transactions go to an OLTP database, and reporting runs from a data warehouse.

### Database roles
- **Database administrator (DBA):** security, backup, recovery, performance.
- **Data engineer:** builds pipelines, moves and transforms data, creates data platforms.
- **Data analyst:** creates reports, performs analysis, builds dashboards.

### File formats
- **CSV:** simple tabular text.
- **JSON:** semi-structured text with labelled fields.
- **Parquet:** widely used for analytics because it stores data by column. This gives faster reporting and better compression.
- **Avro:** often used in data pipelines.

---

## 2. Analytics in Azure

### Data warehouse
A central store that collects data from several systems for reporting and analysis.

Sources (CRM, ERP, website, Excel files) go into the data warehouse, then into Power BI reports.

Operational systems run the business. The data warehouse analyses it.

### ETL vs ELT
| | ETL | ELT |
|---|---|---|
| Order | Extract, then transform, then load | Extract, then load, then transform |
| Where the cleaning happens | Before the data reaches the destination | After the raw data has been loaded |
| Typical use | Traditional approach | Modern cloud approach, where the platform can process large volumes |

### Data pipeline
A sequence of steps that moves data from source to destination, for example: sales database, ETL process, data warehouse, Power BI. A pipeline can be manual or automated. Data engineers design and maintain pipelines.

### Data lake vs data warehouse
- **Data lake:** raw storage. It can hold CSV, JSON, PDFs, logs, images and streaming data.
- **Data warehouse:** curated business data prepared for reporting.

### Batch vs streaming
| | Batch | Streaming |
|---|---|---|
| When data is processed | On a schedule | Continuously, as it arrives |
| Data | Historical | Live |
| Cost and complexity | Simpler and usually cheaper | More complex and usually costlier |
| Typical use | Daily sales reports, monthly finance reporting | Fraud detection, IoT monitoring, live dashboards |
| Delay | Minutes to hours | Seconds |

### Business intelligence (BI)
Turning data into decisions. Typical flow: applications, data pipeline, data warehouse, Power BI, business decisions.

---

## 3. Relational data (fundamentals only)

- **Tables, rows and columns.**
- **Primary key:** uniquely identifies each row in a table.
- **Foreign key:** links a row to a row in another table.

```text
Customers            Orders
---------            ------
CustomerID           OrderID
Name                 CustomerID   <- links each order to a customer
                     Amount
```

Basic SQL:
```sql
SELECT * FROM Customers;
SELECT Name FROM Customers WHERE City = 'Leeds';
```
Conceptually: `SELECT` reads rows, `INSERT` adds rows, `UPDATE` changes rows, `DELETE` removes rows.

---

## 4. Non-relational data (skim)

- **Key-value:** data stored as a key and its value, for example `"1001": "Alex"`.
- **Document database:** stores JSON documents. Example: Azure Cosmos DB.
- **Graph database:** stores relationships. Example: social networks.

Use non-relational storage when you need a flexible layout, huge scale or rapid application development.

---

## 5. In the hospital project (my mapping; verify against what Dana said)

| Concept | In the no-show project |
|---|---|
| Transactional (OLTP) | The booking system, where appointments are recorded and cancelled |
| Analytical (OLAP) | The no-show figure Dana gives the director |
| Structured data | The booking export and the cardiology spreadsheet |
| Data warehouse | Doesn't exist today. Priya's manual Excel work is a stand-in. |
| Data pipeline | Today: export, then manual matching (a manual pipeline). Possible future: an automatic link. |
| Batch | Priya's export and matching, run whenever leadership asks |
| Streaming | Not confirmed as needed. Dana wants an answer in the meeting, not necessarily live data. This is a hypothesis to test. |

---

## 10 things to remember
1. Structured, semi-structured and unstructured data.
2. Transactional (OLTP) vs analytical (OLAP).
3. What a data warehouse does.
4. What a data lake does.
5. The ETL process.
6. The ELT process.
7. The data pipeline concept.
8. Batch processing.
9. Streaming processing.
10. The BI reporting flow, ending in Power BI.
