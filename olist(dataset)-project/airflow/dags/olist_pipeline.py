from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = Path("/opt/airflow/project")

with DAG(
    dag_id="olist_pipeline",
    description="Load Olist source data and build dbt analytics models",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["olist", "airflow", "dbt"],
) as dag:
    ingest_source_data = BashOperator(
        task_id="ingest_source_data",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python -m src.ingestion.load_olist --data-dir data/raw"
        ),
    )
    build_dbt_models = BashOperator(
        task_id="build_dbt_models",
        bash_command=(
            f"cd {PROJECT_DIR}/dbt/olist && "
            "dbt run --profiles-dir . && dbt test --profiles-dir ."
        ),
    )
    ingest_source_data >> build_dbt_models
