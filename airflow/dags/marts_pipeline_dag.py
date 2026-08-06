
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='marts_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffe', 'etl', 'marts']
) as dag:

    run_marts_pipeline = BashOperator(
        task_id='run_marts_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/marts &&
        PYTHONPATH=/opt/airflow/project python run_marts_load.py
        """,
    )