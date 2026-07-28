#!/usr/bin/env bash
set -euo pipefail

cd /opt/cp3-airflow
docker compose ps
curl -fsS http://127.0.0.1:8080/api/v2/monitor/health
docker compose exec -T airflow-scheduler airflow dags list
systemctl start cp3-dag-sync.service
systemctl is-active cp3-dag-sync.timer

bq --project_id=jcdeah-009 query --use_legacy_sql=false '
CREATE TABLE `jcdeah-009.cp3_airflow._sa_access_test`
AS SELECT CURRENT_TIMESTAMP() AS tested_at;
SELECT COUNT(*) AS row_count FROM `jcdeah-009.cp3_airflow._sa_access_test`;
DROP TABLE `jcdeah-009.cp3_airflow._sa_access_test`;
'

echo "VM verification passed."

