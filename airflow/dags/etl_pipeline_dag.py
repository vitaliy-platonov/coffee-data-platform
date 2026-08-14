
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='etl_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['coffee', 'etl', 'pipeline'],
) as dag:

    run_initial_load = BashOperator(
        task_id='run_initial_load',
        bash_command="""
        cd /opt/airflow/project/src/initial_load &&
        PYTHONPATH=/opt/airflow/project python initial_load.py
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=30),
    )

    run_incremental_load = BashOperator(
        task_id='run_incremental_load',
        bash_command="""
        cd /opt/airflow/project/src/incremental_load &&
        PYTHONPATH=/opt/airflow/project python incremental_pipeline.py
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=30),
    )

    run_raw_pipeline = BashOperator(
        task_id='run_raw_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/raw_layer &&
        PYTHONPATH=/opt/airflow/project python raw_pipeline.py
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=30),
    )

    run_staging_pipeline = BashOperator(
        task_id='run_staging_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/staging_load &&
        PYTHONPATH=/opt/airflow/project python staging_pipeline.py
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=30),
    )

    run_core_pipeline = BashOperator(
        task_id='run_core_pipeline',
        bash_command="""
        cd /opt/airflow/project/src/core_load &&
        PYTHONPATH=/opt/airflow/project python run_core_load.py
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=30),
    )

    run_marts_pipeline = BashOperator(
        task_id='run_marts_pipeline',
        bash_command="""
        cd /opt/airflow/project/dbt &&
        dbt run --log-path /tmp/dbt_logs --target-path /tmp/dbt_target
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=30),
    )

    (
        run_initial_load
        >> run_incremental_load
        >> run_raw_pipeline
        >> run_staging_pipeline
        >> run_core_pipeline
        >> run_marts_pipeline
    )

