use Amazon Redshift for the analytical storage

Redshift Serverless setup screen

# Redshift Layer

This folder contains the SQL scripts for Redshift tables and loading data from S3.

## Files

- `schema/create_tables.sql` : Creates staging, fact, and dimension tables.
- `schema/example_queries.sql` : Example queries for testing analytics.
- `scripts/load_s3_to_redshift.sql` : COPY command to load Parquet data from S3 into Redshift.

## Usage

1. Create Redshift cluster and attach IAM Role with S3 access.
2. Run `create_tables.sql` to setup tables.
3. Use `load_s3_to_redshift.sql` to load sessionized events from S3.
4. Optionally, run dbt transformations on Redshift staging tables.

## With this setup:

- Spark streaming writes sessionized events to S3 (Parquet). 
- Redshift staging table loads S3 Parquet files via COPY. 
- Fact and dimension tables are created in Redshift for analytics. 
- dbt can pick up stg_sessionized_events and transform into analytics star schema. 

# IAM role that Redshift uses to access S3
1️⃣ Check Existing IAM Role for Redshift
- Go to the AWS Console → IAM → Roles.
- Look for a role with Redshift in the trusted entity. Typically it says:
- Trusted entity: Redshift
- Make sure this role has S3 read permissions, like AmazonS3ReadOnlyAccess.
- This is the role you can use as RedshiftS3AccessRole in your COPY command.

2️⃣ Create a New IAM Role for Redshift (if you don’t have one)
- Go to IAM → Roles → Create role.
- Choose AWS service → Redshift as the trusted entity.
- Select Redshift - Customizable or AmazonS3ReadOnlyAccess as policy.
- Give it a name, e.g., RedshiftS3AccessRole.
- Finish creating.

Got it 👍
Below is an **additional README section** you can **append to the same Airflow / Redshift README**.
Same style: **plain English, for understanding**.

---

## 🔐 IAM Role Used by Redshift (Very Important)

### Role Name

```
RedshiftS3Full
```

### ARN

```
arn:aws:iam::478867930203:role/RedshiftS3Full
```

### Purpose

This IAM role allows **Redshift to access S3 on your behalf**.

In simple terms:

> Redshift itself cannot read S3
> IAM Role = permission bridge between Redshift and S3

Without this role:

* `COPY` commands will fail
* Redshift cannot read Parquet / CSV files from S3

---

## 🧠 Where This IAM Role Is Used

This role is used when:

* Loading data from **S3 → Redshift**
* Using the `COPY` command

It is **NOT** used by:

* Spark
* Kafka
* Glue crawlers

It is used **only by Redshift**.

---

## 📥 Loading Data from S3 into Redshift (COPY Command)

To load sessionized data stored in S3 into Redshift, we use:

```sql
COPY stg_sessionized_events
FROM 's3://ecommerce-enriched/sessionized/'
IAM_ROLE 'arn:aws:iam::478867930203:role/RedshiftS3Full'
FORMAT AS PARQUET;
```

---

## 🧩 What This COPY Command Does (Line by Line)

```sql
COPY stg_sessionized_events
```

→ Loads data into the Redshift table
`stg_sessionized_events` (staging table)

```sql
FROM 's3://ecommerce-enriched/sessionized/'
```

→ Reads data from this S3 path
(This is where Spark wrote the output)

```sql
IAM_ROLE 'arn:aws:iam::478867930203:role/RedshiftS3Full'
```

→ Grants Redshift permission to access S3

```sql
FORMAT AS PARQUET;
```

→ Tells Redshift the files are in **Parquet format**

---

## 🏗️ Why We Use a Staging Table (`stg_`)

Best practice in data engineering:

1. Load raw data into **staging table**
2. Transform data into **final analytics tables**

So the flow is:

```
S3 → stg_sessionized_events → sessionized_events
```

This keeps:

* Raw data safe
* Transformations clean
* Debugging easier

---

## 🔄 How This Fits with Airflow

You have **two options**:

### Option 1 — Manual (for learning)

Run the `COPY` command directly in:

```
Redshift Query Editor v2
```

Good for:

* First-time testing
* Debugging permissions

---

### Option 2 — Automated (Production Style)

Airflow runs the same `COPY` command automatically:

```
Airflow DAG
 ├─ Task 1: COPY from S3 → Redshift
 ├─ Task 2: Transform into sessionized_events
```

Airflow uses:

* Redshift connection
* Same IAM role
* Scheduled execution

---

## ❌ Common Errors Related to IAM Role

### Error: Access Denied

Cause:

* Wrong IAM role
* Role not attached to Redshift
* S3 bucket policy missing permissions

### Error: File format mismatch

Cause:

* Data is Parquet but `FORMAT AS CSV` used
* Or vice versa

---

## 🧠 Final Mental Model (Including IAM Role)

```
Spark → writes Parquet to S3
IAM Role → allows Redshift to read S3
Redshift COPY → loads data
Airflow → automates COPY + SQL
```
