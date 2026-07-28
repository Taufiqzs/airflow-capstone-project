"""Minimal example DAG. Students should copy this into their own folder."""

from datetime import datetime

from airflow.sdk import DAG, task


with DAG(
    dag_id="cp3_example_healthcheck",
    description="Checks that the shared CP3 Airflow installation can run tasks.",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["cp3", "example"],
    max_active_runs=1,
) as dag:

    @task
    def show_message():
        print("CP3 Airflow is ready. Replace this task with cloud orchestration.")

    show_message()

