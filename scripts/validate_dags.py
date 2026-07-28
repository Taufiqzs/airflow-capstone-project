#!/usr/bin/env python3
"""Cheap static checks before DAG files reach the scheduler.

This is intentionally not a security sandbox. Only trusted/approved code should
be merged because an Airflow DAG is executable Python.
"""

from __future__ import annotations

import ast
import pathlib
import re
import sys

MAX_FILE_BYTES = 256 * 1024
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_]{2,99}$")


def validate(root: pathlib.Path) -> list[str]:
    errors: list[str] = []
    dag_ids: dict[str, pathlib.Path] = {}
    for path in sorted(root.rglob("*.py")):
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path}: file exceeds {MAX_FILE_BYTES} bytes")
            continue
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (UnicodeDecodeError, SyntaxError) as exc:
            errors.append(f"{path}: {exc}")
            continue

        found_ids: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for keyword in node.keywords:
                if keyword.arg == "dag_id" and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                    found_ids.append(keyword.value.value)
        if not found_ids:
            errors.append(f"{path}: no literal dag_id found")
        for dag_id in found_ids:
            if not ID_PATTERN.fullmatch(dag_id):
                errors.append(f"{path}: invalid dag_id {dag_id!r}; use lowercase letters, numbers, and underscores")
            previous = dag_ids.get(dag_id)
            if previous and previous != path:
                errors.append(f"{path}: duplicate dag_id {dag_id!r}, already used by {previous}")
            dag_ids[dag_id] = path
    return errors


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dags")
    if not root.is_dir():
        print(f"DAG directory not found: {root}", file=sys.stderr)
        return 2
    errors = validate(root)
    if errors:
        print("DAG validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"DAG validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

