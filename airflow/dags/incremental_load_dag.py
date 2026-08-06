
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='incremental_load',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffe', 'etl', 'incremental']
) as dag:

    run_incremental_load = BashOperator(
        task_id='run_incremental_load',
        bash_command="""
            cd /opt/airflow/project/src/incremental_load &&
            PYTHONPATH=/opt/airflow/project python incremental_pipeline.py
        """,
    )