#!/usr/bin/env bash
set -euo pipefail

: "${CP3_DAG_BUCKET:?Set CP3_DAG_BUCKET, for example gs://cp3-airflow-dags-prod}"

project_dir="${CP3_AIRFLOW_DIR:-/opt/cp3-airflow}"
target_dir="${project_dir}/dags/submissions"
# Keep temporary files outside the DAG root so Airflow never parses the
# staging copy while a sync or validation is in progress.
staging_dir="${project_dir}/.dag-sync-staging"

mkdir -p "${target_dir}" "${staging_dir}"
gcloud storage rsync "${CP3_DAG_BUCKET}/submissions" "${staging_dir}" --recursive --delete-unmatched-destination-objects

# Validate before publishing. A bad upload must not replace the last good DAG set.
python3 "${project_dir}/scripts/validate_dags.py" "${staging_dir}"
rsync -a --delete "${staging_dir}/" "${target_dir}/"
