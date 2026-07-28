#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import secrets
try:
    from cryptography.fernet import Fernet
except ImportError as exc:
    raise SystemExit("Install cryptography or generate AIRFLOW_FERNET_KEY inside the Airflow image") from exc

print(f"AIRFLOW_FERNET_KEY={Fernet.generate_key().decode()}")
print(f"AIRFLOW_SECRET_KEY={secrets.token_urlsafe(48)}")
print(f"POSTGRES_PASSWORD={secrets.token_urlsafe(32)}")
PY
