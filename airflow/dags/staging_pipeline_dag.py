
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='staging_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffe', 'etl', 'staging'],
) as dag:

    run_staging_pipeline = BashOperator(
        task_id='run_staging_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/staging_load &&
        PYTHONPATH=/opt/airflow/project python staging_pipeline.py
        """,
    )