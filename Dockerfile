ARG AIRFLOW_VERSION=3.3.0
FROM apache/airflow:${AIRFLOW_VERSION}

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Keep dbt isolated from Airflow's Google provider dependency graph.
COPY dbt-requirements.txt /dbt-requirements.txt
RUN python -m venv /home/airflow/dbt-venv \
    && /home/airflow/dbt-venv/bin/pip install --no-cache-dir -r /dbt-requirements.txt
