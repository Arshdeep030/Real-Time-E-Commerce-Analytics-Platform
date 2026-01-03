from airflow import DAG
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from datetime import datetime
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="redshift_load_dag",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["redshift", "s3", "ecommerce"],
) as dag:

    load_sessionized_to_redshift = S3ToRedshiftOperator(
        task_id="load_sessionized_to_redshift",

        #  Airflow connections
        aws_conn_id="aws_default",
        redshift_conn_id="redshift_default",

        #  S3 source
        s3_bucket="ecommerce-enriched",
        s3_key="sessionized/",

        #  Redshift target
        schema="public",
        table="sessionized_events",

        #  File format
        copy_options=[
            "FORMAT AS PARQUET"
        ],

        method="REPLACE"  
    )
