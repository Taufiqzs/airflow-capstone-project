# Menggunakan dbt di Shared Airflow CP3

Image Airflow menyediakan `dbt-bigquery` pada virtual environment terpisah di `/home/airflow/dbt-venv`. Pemisahan ini mencegah konflik dependensi antara dbt dan provider Google Airflow. dbt dijalankan menggunakan Application Default Credentials dari service account VM, sehingga student tidak perlu dan tidak boleh mengunggah JSON key.

## Struktur submission

```text
dags/submissions/<student_id>/
├── <student_id>_dbt_pipeline.py
└── dbt/
    ├── dbt_project.yml
    ├── profiles.yml
    └── models/
        ├── staging/
        └── marts/
```

`profiles.yml` minimum:

```yaml
cp3:
  target: prod
  outputs:
    prod:
      type: bigquery
      method: oauth
      project: jcdeah-009
      dataset: "{{ env_var('DBT_DATASET') }}"
      location: US
      threads: 2
      timeout_seconds: 300
```

Pada Compute Engine, `method: oauth` memakai Application Default Credentials milik VM. Jangan menambahkan `keyfile`.

## Membuat dataset lalu menjalankan dbt

```python
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.standard.operators.bash import BashOperator

STUDENT_ID = "de_jane"
DBT_DIR = f"/opt/airflow/dags/submissions/{STUDENT_ID}/dbt"

with DAG(
    dag_id=f"{STUDENT_ID}_dbt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
) as dag:
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset",
        project_id="jcdeah-009",
        dataset_id=f"cp3_{STUDENT_ID}",
        location="US",
        exists_ok=True,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        cwd=DBT_DIR,
        env={"DBT_DATASET": f"cp3_{STUDENT_ID}"},
        append_env=True,
        bash_command=(
            "/home/airflow/dbt-venv/bin/dbt deps --profiles-dir . "
            "&& /home/airflow/dbt-venv/bin/dbt build --profiles-dir ."
        ),
    )

    create_dataset >> dbt_build
```

## Batasan dan aturan

- Dataset wajib bernama `cp3_<student_id>`, lowercase dan underscore saja.
- Lokasi contoh adalah `US`; ubah hanya jika seluruh data yang dipakai berada di lokasi lain.
- Service account Airflow dibagi oleh seluruh student. Secara teknis semua DAG memiliki identitas yang sama, jadi jangan mengakses dataset student lain.
- `dbt build` wajib mencakup test yang relevan, minimal `not_null`, `unique`, atau relationship sesuai model.
- Gunakan maksimum dua thread. Jangan memindahkan pemrosesan besar ke RAM VM Airflow.
- Model besar sebaiknya incremental dan memiliki filter partisi.
- Tambahkan langkah cleanup dataset di README. Penghapusan resource tetap dilakukan secara manual atau melalui DAG terpisah yang hanya dijalankan setelah penilaian.

Untuk isolasi yang lebih kuat, instruktur perlu memberi service account berbeda per student dan IAM hanya pada dataset masing-masing. Instalasi shared saat ini mengutamakan biaya rendah dan kemudahan penggunaan, bukan isolasi antarstudent.
