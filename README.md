# 🧾 User Access Log Analysis & Security Monitoring Dashboard  
*(Docker + Airflow + dbt + PostgreSQL + SQLAlchemy + Faker)*

This project demonstrates a **complete, containerized data pipeline** for analyzing user access and login behavior.  
It combines **Python (SQLAlchemy)**, **PostgreSQL**, **dbt**, **Airflow**, and **Power BI**, all running in **Docker**.  
The synthetic log data is generated automatically using the **Faker** library.

[![Access Log Dashboard](/Resources/images/AccessLog_Thumbnail.png)]()

> ⚠️ All data is **synthetic**, created purely for demonstration and learning purposes.

---

## 👨🏽‍💻 Author  
**[Abdulhafiz Yusuf](https://github.com/Abdulhafiz-Yusuf)**  
Data Engineering & Analytics Enthusiast  
📍 Nigeria | 🎓 M.Sc. Information Technology (NOUN)

---

## 📚 Table of Contents
- [🎯 Project Objective](#-project-objective)
- [🧱 Architecture Overview](#-architecture-overview)
- [🗂️ Data Design](#-data-design)
- [🧰 Data Generation Script](#-data-generation-script)
- [⚙️ Pipeline Components](#️-pipeline-components)
- [🐋 Docker Setup](#-docker-setup)
- [🪶 Airflow DAG Workflow](#-airflow-dag-workflow)
- [📊 Power BI Dashboard](#-power-bi-dashboard)
- [🚀 Run the Project](#-run-the-project)
- [📁 Repository Structure](#-repository-structure)
- [💬 Talking Points](#-talking-points)

---

## 🎯 Project Objective
Analyze **system login and access logs** to detect:
- Repeated failed logins  
- Off-hour access attempts  
- Multiple logins from distinct IP addresses  

This project showcases the **security analytics** capabilities of a modern data engineering stack.

---

## 🧱 Architecture Overview
```text
[generate_access_logs.py] → [Python + SQLAlchemy] → [PostgreSQL] → [dbt Models] → [Airflow DAG] → [Power BI Dashboard]
````

| Layer          | Tool           | Purpose                               |
| -------------- | -------------- | ------------------------------------- |
| Data Source    | Python + Faker | Generate synthetic log data           |
| Ingestion      | SQLAlchemy     | Load CSV into PostgreSQL              |
| Storage        | PostgreSQL     | Persist structured log data           |
| Transformation | dbt            | Derive aggregates and flags           |
| Orchestration  | Airflow        | Automate ETL and transformations      |
| Visualization  | Power BI       | Display user activity & anomalies     |
| Deployment     | Docker         | Run everything in isolated containers |

---

## 🗂️ Data Design

**File:** `/data/access_logs.csv`

| Column      | Example                      | Description             |
| ----------- | ---------------------------- | ----------------------- |
| log_id      | 1                            | Unique log entry ID     |
| user_id     | 112                          | Employee or system user |
| username    | ayusuf                       | User name               |
| login_time  | 2025-10-21 08:15:30          | Login attempt time      |
| logout_time | 2025-10-21 16:30:00          | Logout time             |
| ip_address  | 102.89.44.12                 | Source IP               |
| device_type | Desktop / Mobile             | Device used             |
| status      | SUCCESS / FAILED             | Login status            |
| branch_name | Gusau                        | Branch/office           |
| role        | Teller / Ops / IT / Security | User role category      |

---

## 🧰 Data Generation Script

**File:** `generate_access_logs.py`

This script creates a **realistic synthetic log dataset (500–1000 rows)** using the `Faker` library.

### 📄 Key Features:

* Random users, IPs, branches, and roles
* 92% successful vs 8% failed logins
* Realistic work hours (8 AM – 6 PM)
* Automatic logout timestamps for successful sessions

### 🧠 Code Snippet:

```python
# generate_access_logs.py
# ------------------------------------------------------------
# Hands-on: Create realistic access_logs.csv (500–1000 rows)
# ------------------------------------------------------------
import csv, random
from datetime import datetime, timedelta
from faker import Faker

NUM_ROWS = 750
SEED = 42
OUTPUT_FILE = "access_logs.csv"

random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

USERNAMES = [fake.user_name() for _ in range(120)]
BRANCHES = ["Gusau", "Kano", "Lagos", "Abuja", "Port Harcourt", "Ibadan"]
ROLES = ["Teller", "Ops", "IT", "Security"]
DEVICE_TYPES = ["Desktop", "Mobile"]
STATUSES = ["SUCCESS", "FAILED"]

def random_workday_timestamp(start_hour=8, end_hour=18):
    start = datetime(2025, 1, 1)
    end = datetime(2025, 12, 31)
    random_day = start + timedelta(days=random.randint(0, (end - start).days))
    hour, minute, second = random.randint(start_hour, end_hour - 1), random.randint(0, 59), random.randint(0, 59)
    return random_day.replace(hour=hour, minute=minute, second=second, microsecond=0)

rows = []
for log_id in range(1, NUM_ROWS + 1):
    username = random.choice(USERNAMES)
    user_id = USERNAMES.index(username) + 100
    login_time = random_workday_timestamp()
    status = random.choices(STATUSES, weights=[0.92, 0.08])[0]
    logout_time = login_time + timedelta(hours=random.randint(1, 8)) if status == "SUCCESS" else ""

    rows.append({
        "log_id": log_id,
        "user_id": user_id,
        "username": username,
        "login_time": login_time.strftime("%Y-%m-%d %H:%M:%S"),
        "logout_time": logout_time.strftime("%Y-%m-%d %H:%M:%S") if logout_time else "",
        "ip_address": fake.ipv4(),
        "device_type": random.choice(DEVICE_TYPES),
        "status": status,
        "branch_name": random.choice(BRANCHES),
        "role": random.choice(ROLES),
    })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Created {OUTPUT_FILE} with {len(rows)} rows.")
```

✅ Output: `access_logs.csv` (750 rows)

---

## ⚙️ Pipeline Components

### 🧮 Python ETL (SQLAlchemy)

* Creates database & table (`access_logs`)
* Loads CSV data into PostgreSQL
* Runs inside Docker via Airflow

### 🧱 dbt Models

* `stg_access_logs.sql` → clean & normalize raw data
* `agg_user_activity.sql` → summarize login behavior
* `suspicious_activity.sql` → flag off-hour and multi-IP users

### 🪶 Airflow DAG

* `access_log_refresh_dag.py`

  * Task 1: Run Python loader
  * Task 2: Execute dbt models
* Scheduled daily (`@daily`) or on demand.

---

## 🐋 Docker Setup

Uses prebuilt images you already have:

| Service       | Image                     | Purpose                        |
| ------------- | ------------------------- | ------------------------------ |
| PostgreSQL    | `postgres:15`             | Database                       |
| Airflow + dbt | `airflow-with-dbt:latest` | Orchestration & transformation |
| Adminer       | `adminer:latest`          | Web database viewer            |

```bash
# Run everything
docker compose up -d
```

Access:

* Airflow → [http://localhost:8080](http://localhost:8080) (admin/admin)
* Adminer → [http://localhost:8081](http://localhost:8081)

---

## 🪶 Airflow DAG Workflow

1️⃣ **Load CSV into PostgreSQL**

```python
PythonOperator(
    task_id="load_access_logs",
    python_callable=run_sqlalchemy_loader
)
```

2️⃣ **Run dbt Models**

```bash
dbt run --project-dir /opt/airflow/dbt
```

---

## 📊 Power BI Dashboard

| Page                    | Insights                                |
| ----------------------- | --------------------------------------- |
| **Access Overview**     | Total logins, failed rate, device usage |
| **User Activity**       | Success vs failure by user/role         |
| **Suspicious Behavior** | Off-hour & multi-IP logins by branch    |

**Connect Power BI:**

```
Host: localhost
Port: 5432
Database: airflow
Username: airflow
Password: airflow
```

---

## 🚀 Run the Project

### Step-by-Step

```bash
# 🧭 HOW TO RUN
# ------------------------------------------------------------
# 1️⃣ Create directories
#     mkdir -p dags logs plugins dbt_project data
#
# 2️⃣ Generate fake CSV
#     python3 generate_access_logs.py
#
# 3️⃣ Initialize Airflow
#     docker compose up airflow-init
#
# 4️⃣ Start the full stack
#     docker compose up -d
#
# 5️⃣ Access:
#     Airflow UI → http://localhost:8081
#     Adminer UI → http://localhost:8083
#
# Login:
#     Airflow: admin / admin
#     Adminer: Server=postgres, User=${POSTGRES_USER}, Pass=${POSTGRES_PASSWORD}
# ------------------------------------------------------------
```

---

## 📁 Repository Structure

```
access_log_analysis/
├── data/
│   └── access_logs.csv
├── dags/
│   ├── access_log_refresh_dag.py
│   └── load_access_logs_sqlalchemy.py
├── dbt/
│   └── models/
│       ├── stg_access_logs.sql
│       ├── agg_user_activity.sql
│       └── suspicious_activity.sql
├── generate_access_logs.py
├── docker-compose.yml
├── .env
├── .env.template
└── README.md
```

---

## 💬 Talking Points (for Internal Interview)

> “I built a **Dockerized security monitoring pipeline** that generates synthetic access logs, loads them into PostgreSQL using SQLAlchemy, transforms them with dbt, and automates everything through Airflow.
> Finally, I visualize risky login behavior in Power BI — helping identify failed logins, off-hour access, and users with multiple IP addresses.”

---

## ⚡ Tech Stack

* **Python + SQLAlchemy + Faker** → Data generation & ingestion
* **PostgreSQL 15** → Central data storage
* **dbt** → Transformations & analytics models
* **Airflow** → Scheduling & orchestration
* **Docker Compose** → Unified environment
* **Power BI** → Visualization & KPI dashboard

---

## 🔒 Disclaimer

All datasets are **synthetic and anonymized**.
No real user, customer, or institutional data was used.

---

**🧠 Insight:**
This project merges **data engineering**, **security analytics**, and **ETL automation**, reflecting the same skill set required for a **Data Analyst (Information Security)** role.
