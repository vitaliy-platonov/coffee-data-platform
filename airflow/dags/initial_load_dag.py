
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='initial_load',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffe', 'etl', 'initial_load'],
) as dag:

    run_initial_load = BashOperator(
        task_id='run_initial_load',
        bash_command="""
        cd /opt/airflow/project/src/initial_load &&
        PYTHONPATH=/opt/airflow/project python initial_load.py
        """,
    )