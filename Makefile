.PHONY: prepare build init up down restart status logs validate

prepare:
	mkdir -p dags/submissions logs plugins config
	test -f .env || (cp .env.example .env && echo "Edit .env before continuing" && false)

build:
	docker compose build

init:
	docker compose up airflow-init

up:
	docker compose up -d postgres airflow-api-server airflow-scheduler airflow-dag-processor

down:
	docker compose down

restart:
	docker compose restart airflow-api-server airflow-scheduler airflow-dag-processor

status:
	docker compose ps

logs:
	docker compose logs --tail=200

validate:
	python3 scripts/validate_dags.py dags

