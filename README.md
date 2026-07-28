# CP3 Shared Airflow

Airflow ringan untuk mengorkestrasi Capstone Project 3 berbasis cloud. Stack ini ditujukan untuk satu VM GCP `e2-medium` Spot (2 vCPU, 4 GB RAM). Airflow hanya mengorkestrasi job; pemrosesan berat harus dijalankan di BigQuery, Dataflow, Dataproc, atau layanan cloud setara.

## Arsitektur

```text
Student pull request -> review -> merge ke main
                                -> GitHub-hosted Actions
                                -> GCS bucket /submissions
                                -> systemd timer pada VM
                                -> dags/submissions
                                -> Airflow LocalExecutor
                                -> layanan cloud milik student
```

Komponen runtime:

- Airflow 3 API server, scheduler, dan DAG processor.
- PostgreSQL 16 sebagai metadata database.
- LocalExecutor dengan maksimum dua task paralel.
- GCS sebagai jalur deployment DAG yang tahan terhadap Spot preemption.
- UI hanya bind ke `127.0.0.1:8080`; akses menggunakan IAP/SSH tunnel.

## Mulai secara lokal

1. Salin `.env.example` menjadi `.env`.
2. Generate secret dengan `./scripts/generate_secrets.sh`, lalu masukkan hasilnya ke `.env`.
   Pada Linux, set `AIRFLOW_UID` ke hasil `id -u` user yang menjalankan project.
3. Jalankan `make build`, `make init`, lalu `make up`.
4. Ambil password admin yang dibuat Simple Auth Manager dari `config/simple_auth_manager_passwords.json.generated`.
5. Periksa dengan `make status` dan buka `http://localhost:8080`.

Jangan gunakan nilai `CHANGE_ME` atau `GENERATE_ME` pada deployment sebenarnya. Simple Auth Manager cocok untuk instalasi kelas yang UI-nya dilindungi IAP/SSH tunnel; jangan membuka UI ke internet.

## Struktur submission

Setiap student menyimpan file di:

```text
dags/submissions/<student_id>/<student_id>_<nama_pipeline>.py
```

Gunakan `dag_id` unik dengan awalan student ID, misalnya `de_jane_taxi_batch`. DAG baru selalu paused agar instruktur dapat memeriksanya sebelum dijalankan.

## Dokumentasi

- [BUILD_STEPS.md](docs/BUILD_STEPS.md): langkah yang dilakukan saat membangun project ini.
- [VM_SETUP.md](docs/VM_SETUP.md): pembuatan VM dan instalasi.
- [GITHUB_DEPLOYMENT.md](docs/GITHUB_DEPLOYMENT.md): GitHub Actions, WIF, GCS, dan sinkronisasi.
- [STUDENT_GUIDE.md](docs/STUDENT_GUIDE.md): aturan penulisan dan pengumpulan DAG.
- [DBT_USAGE.md](docs/DBT_USAGE.md): menjalankan project dbt dan membuat dataset BigQuery dari DAG.
- [OPERATIONS.md](docs/OPERATIONS.md): operasi, recovery Spot VM, backup, dan troubleshooting.
- [SECURITY.md](docs/SECURITY.md): batas kepercayaan dan keamanan minimum.
- [DEPLOYMENT_JCDEAH_009.md](docs/DEPLOYMENT_JCDEAH_009.md): resource aktual, status verifikasi, dan perintah akses deployment saat ini.
