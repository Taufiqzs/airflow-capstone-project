# Deployment Aktual - jcdeah-009

Deployment dibuat pada 28 Juli 2026.

## Resource

| Resource | Nilai |
| --- | --- |
| GCP project | `jcdeah-009` |
| VM | `cp3-airflow-b` |
| Zone | `us-central1-b` |
| Machine | `e2-medium` Spot, 2 vCPU, 4 GB RAM |
| Disk | 30 GB `pd-standard` |
| External IP | Tidak ada |
| Service account | `cp3-airflow-vm@jcdeah-009.iam.gserviceaccount.com` |
| BigQuery dataset | `jcdeah-009.cp3_airflow` |
| DAG bucket | `gs://jcdeah-009-cp3-airflow-dags` |
| Firewall | `cp3-airflow-allow-iap-ssh` |
| GitHub deploy service account | `cp3-github-deployer@jcdeah-009.iam.gserviceaccount.com` |
| Workload Identity Pool | `cp3-github` / provider `github` |

Service account mendapat `roles/bigquery.jobUser` dan `roles/bigquery.user` pada project, `roles/bigquery.dataEditor` pada dataset bersama `cp3_airflow`, dan `roles/storage.objectViewer` hanya pada bucket DAG. Role `bigquery.user` memungkinkan DAG membuat dataset baru. Karena seluruh DAG memakai service account yang sama, ini bukan isolasi IAM per student; gunakan konvensi `cp3_<student_id>`, review DAG, dan service account per student bila diperlukan isolasi yang kuat.

## Status verifikasi

- API server, scheduler, DAG processor, dan PostgreSQL sehat.
- `cp3_example_healthcheck` berhasil diparse dan dalam keadaan paused.
- Timer sinkronisasi GCS aktif.
- Pengujian BigQuery menggunakan service account VM berhasil membuat, membaca, dan menghapus tabel uji.
- `dbt-bigquery` versi `1.12.0` tersedia terisolasi di `/home/airflow/dbt-venv`.
- Pengujian izin dataset berhasil membuat lalu menghapus `jcdeah-009.cp3_permission_test`.
- External IP sudah dihapus; SSH dan UI hanya diakses melalui IAP tunnel.
- Password admin awal yang tercetak saat startup sudah dirotasi.

## Akses UI

```bash
gcloud compute ssh cp3-airflow-b \
  --project=jcdeah-009 \
  --zone=us-central1-b \
  --tunnel-through-iap \
  -- -L 8080:localhost:8080
```

Buka `http://localhost:8080`. Username adalah `admin`.

Ambil password langsung melalui SSH agar tidak masuk repository atau dokumentasi:

```bash
gcloud compute ssh cp3-airflow-b \
  --project=jcdeah-009 \
  --zone=us-central1-b \
  --tunnel-through-iap \
  --command='sudo cat /opt/cp3-airflow/config/simple_auth_manager_passwords.json.generated'
```

## Spot preemption

Jika status VM menjadi `TERMINATED`, hidupkan kembali dengan:

```bash
gcloud compute instances start cp3-airflow-b \
  --project=jcdeah-009 \
  --zone=us-central1-b
```

Kapasitas Spot tidak dijamin. Setelah VM berhasil hidup, systemd otomatis menjalankan Airflow dan sinkronisasi DAG.

## GitHub Actions

Workload Identity Federation telah dibatasi pada repository `riodpp/airflow-capstone-project`. Workflow `.github/workflows/deploy-dags.yml` memvalidasi submission pada pull request dan menyinkronkan DAG ke bucket setelah perubahan masuk ke `main`.
