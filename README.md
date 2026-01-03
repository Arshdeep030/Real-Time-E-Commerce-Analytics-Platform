
# Real-Time E-Commerce Analytics Platform

An **end-to-end real-time data engineering platform** that simulates e-commerce traffic, processes streaming events, applies analytics-ready transformations, and delivers **business-critical insights through dashboards**.

This project demonstrates **production-grade data engineering** using **Kafka, Spark Structured Streaming, Airflow, dbt, Amazon Redshift, and Grafana**.

---

##  What This Project Solves

Modern e-commerce platforms require:

* Real-time visibility into user behavior
* Reliable, scalable streaming pipelines
* Analytics-ready dimensional models
* Business-facing dashboards for decision-making

This project builds the **complete pipeline** — from **event generation** to **executive dashboards**.

---

##  Architecture Overview

```
Kafka (Event Stream)
   ↓
Spark Structured Streaming (Sessionization & Aggregation)
   ↓
Amazon Redshift (Data Warehouse)
   ↓
dbt (Transformations, Tests & Docs)
   ↓
Apache Airflow (Orchestration)
   ↓
Grafana (Business Dashboards)
```

---

## Tech Stack

| Layer             | Technology                          |
| ----------------- | ----------------------------------- |
| Event Streaming   | Apache Kafka                        |
| Stream Processing | Apache Spark (Structured Streaming) |
| Orchestration     | Apache Airflow                      |
| Data Warehouse    | Amazon Redshift                     |
| Transformations   | dbt                                 |
| Data Quality      | dbt Tests                           |
| Visualization     | Grafana                             |
| Infrastructure    | Docker & Docker Compose             |
| Languages         | Python, SQL                         |

---

##  Project Structure

```
├── airflow/                    # Orchestration layer
│   ├── dags/
│   │   ├── redshift_analytics_dag.py
│   │   ├── redshift_load_dag.py
│   │   └── redshift_session_dag.py
│   └── sql/                    # SQL used by Airflow operators
│       ├── check_fact_user_sessions.sql
│       ├── dim_time.sql
│       ├── dim_users.sql
│       └── fact_user_sessions.sql
│
├── data_generator/             # Real-time traffic simulation
│   ├── producer.py             # Kafka producer
│   ├── requirements.txt
│   └── readme.md
│
├── dbt/                        # Transformation layer
│   ├── models/
│   │   ├── staging/
│   │   │   ├── schema.yml
│   │   │   └── stg_sessionized_events.sql
│   │   └── marts/
│   │       ├── dim_time.sql
│   │       ├── dim_users.sql
│   │       ├── fact_user_sessions.sql
│   │       └── fct_conversion_funnel.sql
│   ├── screenshots/
│   │   ├── dbt_lineage_medallion.png
│   │   └── dbt_tests_passed.png
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── grafana/                    # Visualization layer
│   ├── queries/
│   │   ├── active_users.sql
│   │   ├── conversion_funnel.sql
│   │   ├── daily_revenue.sql
│   │   ├── funnel_efficiency.sql
│   │   └── total_revenue.sql
│   ├── screenshots/
│   │   ├── active_users_events.png
│   │   ├── conversion_funnel.png
│   │   ├── daily_revenue.png
│   │   ├── funnel_efficiency.png
│   │   └── total_revenue.png
│   └── readme.md
│
├── kafka/                      # Streaming infrastructure
│   ├── create_topics.sh
│   └── docker-compose.yml
│
├── spark/                      # Stream processing
│   ├── streaming/
│   │   ├── sessionization.py
│   │   └── schema.py
│   └── batch/
│       └── daily_aggregations.py
│
├── docker-compose.yml          # Full stack deployment
├── Dockerfile                  # Custom Airflow/Spark image
└── README.md
```

---

##  Data Flow Explained

###  Data Generation (Kafka)

* `producer.py` simulates:

  * Page views
  * Add-to-cart events
  * Purchases
* Events are pushed to Kafka topics in real time

---

###  Stream Processing (Spark)

* Sessionization groups events by user sessions
* Streaming jobs enrich events and load data into Redshift
* Batch jobs compute daily aggregates

---

###  Orchestration (Airflow)

Airflow manages:

* Redshift loading
* dbt model execution
* Data quality validation

**Core DAG:**

```
redshift_analytics_dag
```

---

###  Transformation & Modeling (dbt)

**Staging Layer**

* Cleans and standardizes raw events

**Mart Layer**

* `fact_user_sessions` – session-level engagement
* `fct_conversion_funnel` – revenue & conversion metrics
* `dim_users` – user attributes
* `dim_time` – time intelligence

**Data Quality**

* `not_null`
* `unique`
* Referential integrity tests

---

###  Visualization (Grafana)

Dashboards include:

* Total Revenue
* Active Users
* Daily Revenue Trends
* Conversion Funnel
* Funnel Efficiency %

SQL queries are stored under:

```
grafana/queries/
```

Screenshots are included as proof of execution.

---

## Example Business Insights

* Conversion rate tracking
* Funnel drop-off analysis
* Active user monitoring
* Day-over-day revenue growth

---

## Documentation

Generate dbt documentation:

```bash
dbt docs generate
dbt docs serve
```

Includes:

* Full lineage graph
* Column-level metadata
* Model descriptions

---

##  Data Quality & Reliability

* Automated dbt tests
* Airflow task retries & logging
* Idempotent transformations
* Modular, scalable architecture

---

## How to Run the Project

### Start Kafka

```bash
cd kafka
docker compose up -d
```

---

### Start Data Generator

```bash
cd data_generator
python producer.py
```

---

### Run Spark Streaming Job

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1,org.apache.hadoop:hadoop-aws:3.2.2 \
  spark/streaming/sessionization.py
```

---

### Start Airflow

```bash
cd airflow
docker-compose up -d
```

Initialize (first run only):

```bash
docker-compose run airflow-webserver airflow db init
```

---

### Run dbt Locally

```bash
cd dbt
dbt clean
dbt debug
dbt test
```

---

### Trigger Airflow DAG

```bash
airflow dags unpause redshift_analytics_dag
airflow dags trigger redshift_analytics_dag
```

---

### Start Grafana

```bash
brew services start grafana
```

---



