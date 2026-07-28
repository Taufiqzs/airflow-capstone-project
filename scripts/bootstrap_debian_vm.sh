#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script with sudo." >&2
  exit 1
fi

source_dir="${1:?Usage: bootstrap_debian_vm.sh SOURCE_DIR}"
install_dir="/opt/cp3-airflow"
airflow_user="cp3airflow"

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl gnupg rsync openssl

install -m 0755 -d /etc/apt/keyrings
if [[ ! -f /etc/apt/keyrings/docker.asc ]]; then
  curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
  chmod a+r /etc/apt/keyrings/docker.asc
fi
. /etc/os-release
cat > /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: ${VERSION_CODENAME}
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

if [[ ! -f /usr/share/keyrings/cloud.google.gpg ]]; then
  curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | gpg --dearmor --yes -o /usr/share/keyrings/cloud.google.gpg
fi
cat > /etc/apt/sources.list.d/google-cloud-sdk.list <<'EOF'
deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main
EOF

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin google-cloud-cli
systemctl enable --now docker

if ! id "${airflow_user}" >/dev/null 2>&1; then
  useradd --system --uid 50000 --home-dir "${install_dir}" --shell /usr/sbin/nologin "${airflow_user}"
fi

mkdir -p "${install_dir}"
rsync -a --delete --exclude='.env' "${source_dir}/" "${install_dir}/"
mkdir -p "${install_dir}/dags/submissions" "${install_dir}/logs" "${install_dir}/plugins" "${install_dir}/config"

postgres_password="$(openssl rand -hex 24)"
fernet_key="$(openssl rand -base64 32 | tr '+/' '-_')"
secret_key="$(openssl rand -hex 32)"

cat > "${install_dir}/.env" <<EOF
AIRFLOW_IMAGE_NAME=cp3-airflow:3.3.0
AIRFLOW_UID=50000
AIRFLOW_ADMIN_USERNAME=admin
POSTGRES_USER=airflow
POSTGRES_PASSWORD=${postgres_password}
POSTGRES_DB=airflow
AIRFLOW_FERNET_KEY=${fernet_key}
AIRFLOW_SECRET_KEY=${secret_key}
AIRFLOW_PARALLELISM=2
AIRFLOW_MAX_ACTIVE_TASKS_PER_DAG=2
AIRFLOW_MAX_ACTIVE_RUNS_PER_DAG=1
AIRFLOW_DAG_PROCESSOR_PARSING_PROCESSES=1
EOF
chmod 0600 "${install_dir}/.env"

mkdir -p /etc/cp3-airflow
cat > /etc/cp3-airflow/dag-sync.env <<'EOF'
CP3_DAG_BUCKET=gs://jcdeah-009-cp3-airflow-dags
CP3_AIRFLOW_DIR=/opt/cp3-airflow
EOF
chmod 0640 /etc/cp3-airflow/dag-sync.env

chown -R "${airflow_user}:${airflow_user}" "${install_dir}"
chmod +x "${install_dir}/scripts/"*.sh "${install_dir}/scripts/"*.py

cp "${install_dir}/systemd/cp3-airflow.service" /etc/systemd/system/
cp "${install_dir}/systemd/cp3-dag-sync.service" /etc/systemd/system/
cp "${install_dir}/systemd/cp3-dag-sync.timer" /etc/systemd/system/
systemctl daemon-reload

cd "${install_dir}"
docker compose build
docker compose up airflow-init
docker compose up -d postgres airflow-api-server airflow-scheduler airflow-dag-processor

systemctl enable cp3-airflow.service cp3-dag-sync.timer
systemctl start cp3-dag-sync.timer

echo "Bootstrap completed. Retrieve the generated admin password from:"
echo "${install_dir}/config/simple_auth_manager_passwords.json.generated"

