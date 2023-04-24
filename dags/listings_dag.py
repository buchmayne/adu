from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from src.scrape_zillow import scrape_zillow
from config import get_connection

engine = get_connection()

with DAG(
    "listings_dag",
    start_date=datetime(2023, 2, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    scrape_zillow = PythonOperator(
        task_id="scrape_zillow",
        python_callable=scrape_zillow,
        op_kwargs={"engine": engine},
    )

    insert_tbl_transformed_zillow_rental_listings = PostgresOperator(
        task_id="insert_tbl_transformed_zillow_rental_listings",
        postgres_conn_id="adu_postgres_conn_id",
        sql="sql/insert_tbl_transformed_zillow_rental_listings.sql",
    )

    scrape_zillow >> insert_tbl_transformed_zillow_rental_listings
