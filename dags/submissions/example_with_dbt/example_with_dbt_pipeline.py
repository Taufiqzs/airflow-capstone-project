"""Contoh submission CP3 dengan dbt Core dan BigQuery."""

from datetime import datetime

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PROJECT_ID = "jcdeah-009"
STUDENT_ID = "example_with_dbt"
DATASET_ID = f"cp3_{STUDENT_ID}"
LOCATION = "asia-southeast2"
DBT_PROJECT_DIR = f"/opt/airflow/dags/submissions/{STUDENT_ID}/dbt"
DBT_BIN = "/home/airflow/dbt-venv/bin/dbt"


with DAG(
    dag_id="example_with_dbt_pipeline",
    description="Contoh CP3 yang menjalankan dbt build ke BigQuery",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["cp3", "example", "dbt", "bigquery"],
) as dag:
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset",
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        location=LOCATION,
        exists_ok=True,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        cwd=DBT_PROJECT_DIR,
        env={
            "DBT_PROJECT_ID": PROJECT_ID,
            "DBT_DATASET": DATASET_ID,
            "DBT_LOCATION": LOCATION,
        },
        append_env=True,
        bash_command=(
            "rm -rf /tmp/dbt-example-with-dbt "
            "&& mkdir -p /tmp/dbt-example-with-dbt/target /tmp/dbt-example-with-dbt/logs "
            f"&& {DBT_BIN} build --profiles-dir . "
            "--target-path /tmp/dbt-example-with-dbt/target "
            "--log-path /tmp/dbt-example-with-dbt/logs"
        ),
    )

    create_dataset >> dbt_build
