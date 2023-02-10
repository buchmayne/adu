from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from src.get_permits import get_permits
from src.add_adu_permits_to_db import add_adu_permits_to_db

with DAG(
    "permits_dag",
    start_date=datetime(2023, 2, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    get_permits = PythonOperator(task_id="get_permits", python_callable=get_permits)

    add_adu_permits_to_db = PythonOperator(
        task_id="add_adu_permits_to_db", python_callable=add_adu_permits_to_db
    )

    get_permits >> add_adu_permits_to_db
