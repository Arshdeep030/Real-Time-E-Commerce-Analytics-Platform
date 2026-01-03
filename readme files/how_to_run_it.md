# Real-Time E-Commerce Analytics Platform

---

##  Architecture Overview

**Flow:**

1. **Kafka** – Ingests real-time e-commerce events
2. **Python Data Generator** – Produces synthetic events
3. **Spark Structured Streaming** – Sessionization & aggregations
4. **Amazon Redshift** – Analytical data warehouse
5. **dbt** – Transformations, tests, documentation
6. **Apache Airflow** – Orchestration & scheduling
7. **Grafana** – Monitoring & visualization

---


##  Prerequisites

* Python 3.9+
* Docker & Docker Compose
* Apache Spark 4.x
* dbt Core (with Redshift adapter)
* Apache Airflow 3.x
* Homebrew (macOS)
* Amazon Redshift cluster

---

##  How to Run the Project (Step-by-Step)

###  Start Kafka

```bash
cd kafka
docker compose up -d
```

Verify:

```bash
docker ps
```

---

###  Start Data Generator

```bash
cd data_generator
python producer.py
```

This continuously produces synthetic e-commerce events to Kafka.

---

###  Run Spark Streaming Job

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1,org.apache.hadoop:hadoop-aws:3.2.2 \
  spark/streaming/sessionization.py
```

This performs real-time sessionization and writes data to Redshift.

---

###  Start Airflow

```bash
cd airflow
docker-compose up -d
```

Initialize metadata DB (first run only):

```bash
docker-compose run airflow-webserver airflow db init
```

List DAGs:

```bash
docker exec airflow-airflow-webserver-1 airflow dags list
```

---

###  Run dbt Locally (Validation)

```bash
cd dbt

dbt clean
dbt debug
dbt ls
dbt test
```

Generate docs:

```bash
dbt docs generate
dbt docs serve --port 8084
```

---

###  Trigger Airflow DAG

```bash
airflow dags unpause redshift_analytics_dag
airflow dags trigger redshift_analytics_dag
```

Check runs:

```bash
airflow dags list-runs redshift_analytics_dag
```

Logs are viewed via **Airflow UI**:
 [http://localhost:8080](http://localhost:8080)

---

###  Start Grafana

```bash
brew services start grafana
```

Access:
[http://localhost:3000](http://localhost:3000)

---

##  dbt Models

* **Staging models** – Cleaned raw events
* **Mart models** – Session-level & revenue analytics
* **Tests** – Not null, unique, accepted values
* **Docs** – Auto-generated lineage & descriptions

---

##  Airflow DAG Flow

```
dbt_run_staging
      ↓
dbt_run_marts
      ↓
dbt_test
```

Retries and logging handled via Airflow 3.x UI.

---

##  Key Learnings

* End-to-end real-time pipeline design
* Spark sessionization logic
* dbt best practices (staging → marts)
* Airflow 3.x orchestration
* Dockerized local data stack

---

##  Resume Bullet

> Built an end-to-end real-time e-commerce analytics platform using Kafka, Spark Structured Streaming, dbt, Airflow, Redshift, and Grafana, enabling sessionized analytics, automated transformations, and production-grade orchestration.

---

## Future Enhancements

* Incremental dbt models
* CI/CD for dbt & Airflow
* Data quality alerts
* Cost-optimized Redshift schemas

---

