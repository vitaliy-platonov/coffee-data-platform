from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="marts_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["coffee", "dbt", "marts"],
) as dag:

    run_marts_pipeline = BashOperator(
        task_id="run_marts_pipeline",
        bash_command="""
        cd /opt/airflow/project/dbt &&
        dbt run --log-path /tmp/dbt_logs --target-path /tmp/dbt_target
        """,
    )