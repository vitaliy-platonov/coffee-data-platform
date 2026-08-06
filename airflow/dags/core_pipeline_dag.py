
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='core_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffe', 'etl', 'core']
) as dag:

    run_core_pipeline = BashOperator(
        task_id='run_core_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/core_load &&
        PYTHONPATH=/opt/airflow/project python run_core_load.py
        """,
    )