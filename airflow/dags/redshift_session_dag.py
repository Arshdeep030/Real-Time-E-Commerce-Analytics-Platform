from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="redshift_session_automation",
    start_date=datetime(2024, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    default_args=default_args,
    tags=["redshift", "sessions"],
) as dag:

    create_sessions = SQLExecuteQueryOperator(
        task_id="create_sessionized_events",
        conn_id="redshift_default",
        sql="""
        CREATE OR REPLACE TABLE public.sessionized_events AS
        WITH ordered_events AS (
            SELECT custid, pdate, amount,
                   LAG(pdate) OVER (PARTITION BY custid ORDER BY pdate) AS prev_time
            FROM public.purchases_internal
        ),
        session_flags AS (
            SELECT *,
                   CASE
                       WHEN prev_time IS NULL THEN 1
                       WHEN DATEDIFF(minute, prev_time, pdate) > 30 THEN 1
                       ELSE 0
                   END AS is_new_session
            FROM ordered_events
        ),
        session_ids AS (
            SELECT *,
                   SUM(is_new_session) OVER (
                       PARTITION BY custid ORDER BY pdate
                       ROWS UNBOUNDED PRECEDING
                   ) AS session_id
            FROM session_flags
        )
        SELECT
            custid,
            session_id,
            MIN(pdate) AS session_start,
            MAX(pdate) AS session_end,
            COUNT(*) AS purchase_count,
            SUM(amount) AS total_amount
        FROM session_ids
        GROUP BY custid, session_id;
        """
    )
