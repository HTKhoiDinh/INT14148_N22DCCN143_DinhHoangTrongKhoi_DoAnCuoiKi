# Distributed SQL Injection Firewall - Query Guard

N22DCCN143 - Dinh Hoang Trong Khoi

## 1. Project Overview

**Query Guard** is a config-driven middleware for protecting a distributed database system from SQL Injection attacks and unauthorized fragment access.

The system sits between the client and multiple distributed database sites. Instead of allowing users to directly access database files, every SQL query must pass through the Query Guard middleware. The middleware analyzes the SQL query, checks security policies, identifies the target data fragment, verifies user access permission, routes the query to the correct site, executes a safe parameterized query, and records the action in an audit log.

This project is based on the topic:

**#109 - Distributed SQL Injection Firewall: "Query Guard"**

---

## 2. Main Features

* Flask-based Web Interface
* Config-driven Middleware Design
* SQL Injection Detection
* Forbidden Keyword and Pattern Blocking
* Distributed Query Routing
* Horizontal Fragmentation
* User-to-Site Access Control
* Three Distributed SQLite Sites
* Security Policy Configuration
* Audit Logging with Query Hash
* Clean/Malicious SQL Dataset Evaluation
* Confusion Matrix and Evaluation Charts

---

## 3. System Architecture

```text
Client Web UI
     |
     v
+-----------------------------+
| Query Guard Middleware      |
|-----------------------------|
| SQL Normalizer              |
| SQL Injection Detector      |
| SQL Parser                  |
| Fragment Metadata Manager   |
| User Policy Manager         |
| Query Router                |
| Safe Query Executor         |
| Audit Logger                |
+-----------------------------+
     |            |            |
     v            v            v
+---------+  +---------+  +---------+
| Site 1  |  | Site 2  |  | Site 3  |
| SQLite  |  | SQLite  |  | SQLite  |
+---------+  +---------+  +---------+
```

The middleware does not hard-code the site routing logic. Instead, it reads configuration files from the `config/` folder.

---

## 4. Config-driven Design

The project uses three main configuration files:

```text
config/
├── fragment_config.json
├── user_policy.json
└── security_policy.json
```

### 4.1 Fragment Configuration

`fragment_config.json` defines how the Employee table is horizontally fragmented across distributed sites.

```json
{
  "Employee": [
    {
      "site": "site1",
      "site_id": 1,
      "db_path": "database/site1.db",
      "fragment_key": "ID",
      "min": 1,
      "max": 1000
    },
    {
      "site": "site2",
      "site_id": 2,
      "db_path": "database/site2.db",
      "fragment_key": "ID",
      "min": 1001,
      "max": 2000
    },
    {
      "site": "site3",
      "site_id": 3,
      "db_path": "database/site3.db",
      "fragment_key": "ID",
      "min": 2001,
      "max": 3000
    }
  ]
}
```

### 4.2 User Policy

`user_policy.json` defines which user can access which distributed site.

```json
{
  "alice": ["site1"],
  "bob": ["site2"],
  "charlie": ["site3"],
  "auditor": ["site1", "site2", "site3"],
  "admin": ["site1", "site2", "site3"]
}
```

### 4.3 Security Policy

`security_policy.json` defines the SQL security rules used by Query Guard.

The middleware blocks:

* Non-SELECT queries
* Multiple SQL statements
* Destructive keywords such as `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`
* UNION-based extraction
* Boolean-based injection such as `OR 1=1`, `OR TRUE`, `OR '1'='1'`
* Comment injection using `--`, `/*`, `*/`

---

## 5. Distributed Database Design

The project uses three SQLite databases to simulate distributed database sites.

```text
database/
├── site1.db
├── site2.db
└── site3.db
```

The Employee table is horizontally fragmented by `Employee.ID`.

| Site   | Database   | ID Range    | Region  |
| ------ | ---------- | ----------- | ------- |
| Site 1 | `site1.db` | 1 - 1000    | North   |
| Site 2 | `site2.db` | 1001 - 2000 | Central |
| Site 3 | `site3.db` | 2001 - 3000 | South   |

The Employee table schema is:

```text
Employee(
    ID,
    Name,
    Department,
    Region,
    Salary,
    TaxCode,
    HealthStatus,
    BankAccount
)
```

The dataset is synthetically generated for controlled evaluation and demonstration.

---

## 6. Query Processing Flow

When a user submits a SQL query, Query Guard performs the following steps:

```text
1. Receive SQL query from client
2. Normalize SQL string
3. Check security policy
4. Block forbidden patterns or malicious SQL
5. Extract Employee ID from SQL query
6. Locate target fragment using fragment_config.json
7. Check user permission using user_policy.json
8. Execute safe parameterized query on selected site
9. Return result to user
10. Write audit log
```

The middleware does not execute the raw SQL query directly. It extracts the Employee ID and then uses a parameterized query internally.

---

## 7. Installation

### 7.1 Create Virtual Environment

```bash
python -m venv venv
```

### 7.2 Activate Virtual Environment on Windows PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```bash
.\venv\Scripts\Activate.ps1
```

### 7.3 Install Required Libraries

```bash
pip install flask matplotlib pandas sqlparse
```

---

## 8. Create Distributed Database Sites

Run:

```bash
python create_sensitive_sites.py
```

Expected output:

```text
Created database/site1.db: ID 1 - 1000
Created database/site2.db: ID 1001 - 2000
Created database/site3.db: ID 2001 - 3000
All sensitive distributed sites created successfully.
```

To check the generated data:

```bash
python check_sensitive_sites.py
```

---

## 9. Run the Web Application

Run:

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## 10. Demo Test Cases

### 10.1 Valid Query on Site 1

User:

```text
alice
```

SQL:

```sql
SELECT * FROM Employee WHERE ID=100
```

Expected result:

```text
ALLOWED
site1
```

---

### 10.2 Valid Query on Site 2

User:

```text
bob
```

SQL:

```sql
SELECT * FROM Employee WHERE ID=1500
```

Expected result:

```text
ALLOWED
site2
```

---

### 10.3 Valid Query on Site 3

User:

```text
charlie
```

SQL:

```sql
SELECT * FROM Employee WHERE ID=2500
```

Expected result:

```text
ALLOWED
site3
```

---

### 10.4 Unauthorized Fragment Access

User:

```text
alice
```

SQL:

```sql
SELECT * FROM Employee WHERE ID=1001
```

Expected result:

```text
ACCESS DENIED
User 'alice' is not allowed to access site2
```

---

### 10.5 SQL Injection Attack

User:

```text
admin
```

SQL:

```sql
SELECT * FROM Employee WHERE ID=1; DROP TABLE Employee
```

Expected result:

```text
BLOCKED
MULTIPLE_SQL_STATEMENTS
```

---

### 10.6 UNION-based Attack

User:

```text
admin
```

SQL:

```sql
SELECT * FROM Employee UNION SELECT username, password FROM Users
```

Expected result:

```text
BLOCKED
FORBIDDEN_KEYWORD: UNION
```

---

## 11. Evaluation

The project evaluates Query Guard using two SQL datasets:

```text
datasets/
├── clean.sql
└── malicious.sql
```

The clean dataset contains valid SQL queries across three distributed sites.
The malicious dataset contains destructive queries, UNION attacks, boolean-based injection, comment injection, lowercase attack variants, and multiple SQL statements.

Run evaluation:

```bash
python evaluation/evaluate.py
```

The evaluation script reports:

* True Positive
* True Negative
* False Positive
* False Negative
* False Positive Rate
* False Negative Rate
* Accuracy
* Precision
* Recall
* F1-score

It also generates visual outputs:

```text
evaluation/
├── evaluation_result.csv
├── confusion_matrix.png
├── metrics_chart.png
└── query_distribution.png
```

Example evaluation result:

```text
True Negative: 47
True Positive: 50
False Positive: 0
False Negative: 1
```

This means Query Guard correctly allowed 47 clean queries and correctly blocked 50 malicious queries. There was no false positive, and one malicious edge-case query was missed. This false negative is analyzed as a limitation of rule-based detection.

---

## 12. Project Structure

```text
Distributed_SQL_Firewall/
│
├── app.py
├── README.md
│
├── config/
│   ├── fragment_config.json
│   ├── user_policy.json
│   └── security_policy.json
│
├── database/
│   ├── site1.db
│   ├── site2.db
│   └── site3.db
│
├── middleware/
│   ├── config_loader.py
│   ├── detector.py
│   ├── parser.py
│   ├── router.py
│   ├── permission.py
│   ├── executor.py
│   └── logger.py
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── datasets/
│   ├── clean.sql
│   └── malicious.sql
│
├── evaluation/
│   ├── evaluate.py
│   ├── evaluation_result.csv
│   ├── confusion_matrix.png
│   ├── metrics_chart.png
│   └── query_distribution.png
│
├── logs/
│   └── query_log.txt
│
├── create_sensitive_sites.py
└── check_sensitive_sites.py
```

---

## 13. Theoretical Background

This project is related to the following distributed database concepts:

* Distributed database systems
* Horizontal fragmentation
* Distributed query processing
* Query routing
* Metadata-based fragment lookup
* Distributed access control
* Location transparency
* Middleware-based security enforcement

The system follows the idea that the client does not need to know where the data is physically stored. Query Guard hides the distribution of data and automatically routes valid queries to the correct fragment.

---

## 14. Security Model

Query Guard uses a multi-layer security model:

```text
Layer 1: Only SELECT queries are allowed
Layer 2: Forbidden SQL keywords are blocked
Layer 3: Forbidden SQL patterns are blocked
Layer 4: Multiple SQL statements are blocked
Layer 5: SQL parser extracts Employee ID
Layer 6: Fragment metadata maps query to correct site
Layer 7: User policy checks fragment access permission
Layer 8: Parameterized query execution prevents raw SQL execution
Layer 9: Audit log records query result and reason
```

This design reduces dependence on predicting every possible malicious SQL string.

---

## 15. Limitations

* The current prototype focuses on SELECT queries over the Employee table.
* The middleware uses rule-based SQL Injection detection.
* One false negative may appear in edge-case testing, showing that rule-based detection has limitations.
* The system is designed for academic demonstration, not production deployment.
* Future improvements may include SQL AST parsing, machine-learning-based anomaly detection, and real networked database sites.

---


## 16. Repository

GitHub/GitLab Repository:

```text
https://github.com/HTKhoiDinh/INT14148_N22DCCN143_DinhHoangTrongKhoi_DoAnCuoiKi.git
```
