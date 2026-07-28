# Setup VM GCP

## Spesifikasi

- Machine type: `e2-medium`.
- Provisioning model: Spot, termination action `STOP`.
- Region yang hemat: `us-central1`.
- Boot disk: Debian 12 atau Ubuntu 24.04, `pd-standard` 30 GB.
- Service account VM: hanya diberi `roles/storage.objectViewer` pada bucket DAG dan role minimum untuk job yang memang diorkestrasi.
- Jangan membuka port 8080 ke internet.

## Instalasi

1. Buat user sistem `cp3airflow` dan direktori `/opt/cp3-airflow`.
2. Install Docker Engine, Docker Compose plugin, Google Cloud CLI, Git, dan rsync.
3. Salin seluruh project ini ke `/opt/cp3-airflow`.
4. Set owner direktori menjadi `cp3airflow`, kecuali file secret yang hanya dapat dibaca root/service terkait.
5. Salin `.env.example` menjadi `.env`, isi seluruh secret, lalu set `AIRFLOW_UID` ke hasil `id -u cp3airflow`. UID yang sama membuat folder `config`, `dags`, dan `logs` dapat dipakai host serta container tanpa permission yang terlalu longgar.
6. Jalankan `docker compose build`.
7. Jalankan `docker compose up airflow-init` satu kali.
8. Nyalakan API server, lalu baca password admin yang dihasilkan pada `/opt/cp3-airflow/config/simple_auth_manager_passwords.json.generated`.
9. Salin file systemd dari folder `systemd/` ke `/etc/systemd/system/`.
10. Salin `docs/dag-sync.env.example` ke `/etc/cp3-airflow/dag-sync.env` dan isi bucket.
11. Aktifkan `cp3-airflow.service` dan `cp3-dag-sync.timer`.

## Mengakses UI

Gunakan IAP tunnel atau SSH local forwarding:

```bash
gcloud compute ssh VM_NAME --zone ZONE --tunnel-through-iap -- -L 8080:localhost:8080
```

Kemudian buka `http://localhost:8080`. Binding localhost mencegah UI terbuka langsung ke internet.

## Setelah Spot preemption

Termination action `STOP` mempertahankan VM dan persistent boot disk. Ketika kapasitas tersedia, hidupkan VM lagi. Service systemd akan menyalakan Docker Compose dan timer akan mengambil DAG terbaru dari GCS.
