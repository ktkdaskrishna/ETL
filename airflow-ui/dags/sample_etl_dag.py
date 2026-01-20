from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def extract():
    print("Extracting data")


def transform():
    print("Transforming data")


def load():
    print("Loading data")


with DAG(
    dag_id="sample_etl_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["template"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> transform_task >> load_task
