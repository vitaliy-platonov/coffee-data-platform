
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='raw_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffe', 'etl', 'raw'],
) as dag:

    run_raw_pipeline= BashOperator(
        task_id='run_raw_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/raw_layer &&
        PYTHONPATH=/opt/airflow/project python raw_pipeline.py
        """,
    )