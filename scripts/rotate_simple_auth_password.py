#!/usr/bin/env python3
"""Rotate the local Simple Auth admin password without printing the secret."""

import json
import os
import pathlib
import secrets

path = pathlib.Path("/opt/cp3-airflow/config/simple_auth_manager_passwords.json.generated")
temporary = path.with_suffix(".tmp")
temporary.write_text(json.dumps({"admin": secrets.token_urlsafe(24)}), encoding="utf-8")
os.chmod(temporary, 0o600)
temporary.replace(path)
os.chown(path, 50000, 0)
print(f"Password rotated. Retrieve it directly on the VM from {path}")
