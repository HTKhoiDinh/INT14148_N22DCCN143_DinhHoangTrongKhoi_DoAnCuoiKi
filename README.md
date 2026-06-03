# Distributed SQL Injection Firewall - Query Guard
N22DCCN143 - Dinh Hoang Trong Khoi

## 1. Project Overview

Query Guard is a middleware-based SQL Injection Firewall for a simulated distributed database system.

The system sits between the client and distributed database sites. It parses SQL queries, blocks malicious SQL patterns, checks fragment access permission, routes valid queries to the correct site, and logs query activities.

## 2. Features

- Flask Web Interface
- SQL Injection Detection
- Forbidden Pattern Blocking
- SQL Parser
- Horizontal Fragmentation
- Query Routing
- Fragment Access Control
- SQLite Distributed Sites
- Audit Logging
- Evaluation using False Positive Rate and False Negative Rate

## 3. Distributed Database Design

The Employee dataset is horizontally fragmented into two SQLite database sites:

- Site 1: `database/site1.db`
  - Employee ID: 1 to 1000
  - Department: IT

- Site 2: `database/site2.db`
  - Employee ID: 1001 to 2000
  - Department: HR

## 4. User Permission

| User  |   Allowed Site    |
|-------|-------------------|
| alice |      Site 1       |
|  bob  |      Site 2       |
| admin | Site 1 and Site 2 |

## 5. Tech Stack

- Python
- Flask
- SQLite
- Bootstrap
- Regular Expression
- HTML/CSS

## 6. Installation

Create virtual environment:

```bash
python -m venv venv