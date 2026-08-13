
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='sales_pyspark_dag',
    start_date=datetime(2026, 8, 13),
    schedule=None,
    catchup=False,
    tags=['spark', 'marts']
) as dag:

    run_sales_mart = BashOperator(
        task_id='run_sales_mart',
        bash_command=(
            "export PYTHONPATH=/opt/airflow/project && "
            "python /opt/airflow/project/src/spark/sales_mart.py"
        ),
    )