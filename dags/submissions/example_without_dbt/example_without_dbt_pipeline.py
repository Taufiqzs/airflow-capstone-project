"""Contoh submission CP3 tanpa dbt.

DAG membuat dataset dan tabel agregasi menggunakan BigQuery operator langsung.
Ganti STUDENT_ID dan query dengan implementasi project student.
"""

from datetime import datetime

from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryInsertJobOperator,
)
from airflow.sdk import DAG

PROJECT_ID = "jcdeah-009"
STUDENT_ID = "example_without_dbt"
DATASET_ID = f"cp3_{STUDENT_ID}"
LOCATION = "asia-southeast2"


with DAG(
    dag_id="example_without_dbt_pipeline",
    description="Contoh CP3 menggunakan BigQuery operator tanpa dbt",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["cp3", "example", "bigquery"],
) as dag:
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset",
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        location=LOCATION,
        exists_ok=True,
    )

    build_daily_summary = BigQueryInsertJobOperator(
        task_id="build_daily_summary",
        project_id=PROJECT_ID,
        location=LOCATION,
        configuration={
            "query": {
                "query": f"""
                    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.daily_trip_summary`
                    PARTITION BY trip_date
                    CLUSTER BY pickup_zone_id AS
                    SELECT
                      trip_date,
                      pickup_zone_id,
                      COUNT(*) AS trip_count,
                      ROUND(SUM(total_amount), 2) AS total_revenue
                    FROM UNNEST([
                      STRUCT(DATE '2026-07-01' AS trip_date, 1 AS pickup_zone_id, 15.50 AS total_amount),
                      STRUCT(DATE '2026-07-01' AS trip_date, 1 AS pickup_zone_id, 22.00 AS total_amount),
                      STRUCT(DATE '2026-07-01' AS trip_date, 2 AS pickup_zone_id, 18.25 AS total_amount),
                      STRUCT(DATE '2026-07-02' AS trip_date, 1 AS pickup_zone_id, 12.75 AS total_amount)
                    ])
                    GROUP BY trip_date, pickup_zone_id
                """,
                "useLegacySql": False,
            }
        },
    )

    check_output = BigQueryInsertJobOperator(
        task_id="check_output",
        project_id=PROJECT_ID,
        location=LOCATION,
        configuration={
            "query": {
                "query": f"""
                    ASSERT (
                      SELECT COUNT(*)
                      FROM `{PROJECT_ID}.{DATASET_ID}.daily_trip_summary`
                    ) > 0 AS 'daily_trip_summary must contain rows';

                    ASSERT (
                      SELECT COUNTIF(trip_count <= 0 OR total_revenue < 0)
                      FROM `{PROJECT_ID}.{DATASET_ID}.daily_trip_summary`
                    ) = 0 AS 'summary contains invalid metrics';
                """,
                "useLegacySql": False,
            }
        },
    )

    create_dataset >> build_daily_summary >> check_output
