from datetime import datetime, timedelta
import subprocess

from airflow import DAG
from airflow.operators.bash import BashOperator


# Paths (LOCAL dbt setup)
DBT_PROJECT_DIR = "'/Users/arsh/Desktop/Projects/realtime ecomm analytics/dbt'"
DBT_PROFILES_DIR = "'/Users/arsh/Desktop/Projects/realtime ecomm analytics/dbt'" 

default_args = {
    "owner": "arsh",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="redshift_analytics_dag",
    description="Run dbt staging and marts models on Redshift",
    default_args=default_args,
    start_date=datetime(2025, 12, 30),
    schedule="*/5 * * * *",
    max_active_runs=1,  
    catchup=False,
    tags=["dbt", "redshift"],
) as dag:

  
    # Run staging models
    dbt_run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command=(
            f"dbt run "
            f"--select staging "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    
    # Run marts models
    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command=(
            f"dbt run "
            f"--select marts "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    
    # Run tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"dbt test "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    dbt_run_staging >> dbt_run_marts >> dbt_test
