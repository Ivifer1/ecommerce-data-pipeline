"""
DAG: ecommerce_pipeline
Orquesta el pipeline ETL completo: Extract → Transform → Load.
Se ejecuta diariamente.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import sys
sys.path.insert(0, "/opt/airflow/scripts")

from extract import extract_all
from transform import transform_all
from load import load_all


# ─── Configuración del DAG ───
default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    description="Pipeline ETL end-to-end: Fake Store API → PostgreSQL",
    schedule_interval="@daily",           # Ejecutar una vez al día
    start_date=days_ago(1),              # Fecha de inicio
    catchup=False,                       # No ejecutar runs históricos
    tags=["etl", "ecommerce", "junior"], # Tags para organizar en Airflow
) as dag:

    # ─── Tarea 1: Extracción ───
    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_all,
    )

    # ─── Tarea 2: Transformación ───
    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_all,
    )

    # ─── Tarea 3: Carga ───
    task_load = PythonOperator(
        task_id="load_data",
        python_callable=load_all,
    )

    # ─── Definir flujo de dependencias ───
    task_extract >> task_transform >> task_load