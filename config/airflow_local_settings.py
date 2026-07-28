"""Small guardrails for a shared CP3 Airflow installation."""

from datetime import timedelta


def task_policy(task):
    """Cap retries and add a default timeout to protect the 4 GB VM."""
    task.retries = min(task.retries or 0, 2)
    if task.execution_timeout is None:
        task.execution_timeout = timedelta(hours=2)


def dag_policy(dag):
    """Prevent one student DAG from consuming all LocalExecutor slots."""
    dag.max_active_runs = min(dag.max_active_runs or 1, 1)
    dag.max_active_tasks = min(dag.max_active_tasks or 2, 2)

