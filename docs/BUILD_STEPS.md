# Langkah Pembuatan Project

Dokumen ini mencatat keputusan dan langkah yang dilakukan saat menyusun project.

## 1. Menentukan ukuran runtime

- Target dipilih `e2-medium` Spot: 2 vCPU dan 4 GB RAM.
- Airflow dipakai sebagai orchestrator, bukan mesin pemrosesan data.
- LocalExecutor dipilih agar tidak memerlukan Redis dan Celery worker.
- Parallelism dibatasi dua task dan satu active run per DAG.

## 2. Menentukan komponen

- Airflow API server untuk UI/API.
- Scheduler untuk penjadwalan task.
- DAG processor untuk parsing DAG terpisah dari scheduler.
- PostgreSQL 16 untuk metadata.
- Persistent Docker volume untuk database.

## 3. Menyiapkan container

- Membuat `Dockerfile` berbasis image resmi Apache Airflow.
- Menambahkan Google provider versi `22.2.2` melalui `requirements.txt` agar build dapat direproduksi.
- Membuat `docker-compose.yml` dengan health check, restart policy, volume, dan binding UI ke localhost.
- Membuat `.env.example` tanpa secret asli.

## 4. Menambahkan guardrail resource

- Membatasi parallelism global dan per-DAG.
- Membatasi maksimum active run.
- Menambahkan cluster policy untuk maksimum retry dan execution timeout default.
- Menyediakan static DAG validator sebelum file diterbitkan.

## 5. Menentukan deployment DAG

- Pull request student harus direview sebelum merge.
- GitHub-hosted Actions memvalidasi dan mengunggah DAG ke GCS.
- VM menyinkronkan GCS setiap menit melalui systemd timer.
- Sinkronisasi memakai staging directory; file baru dipublikasikan hanya jika validasi lolos.

## 6. Menambahkan operasi VM

- Membuat systemd unit untuk menyalakan stack setelah boot/preemption.
- Membuat systemd timer untuk sinkronisasi DAG.
- Menambahkan dokumentasi setup, keamanan, submission, backup, dan recovery.

## 7. Verifikasi yang perlu dilakukan saat deployment

1. `docker compose config` berhasil.
2. Image berhasil dibangun. Jika Docker daemon tidak tersedia pada komputer pembuat, jalankan verifikasi build ini pada VM sebelum service diaktifkan.
3. Migrasi database dan pembuatan admin berhasil.
4. Semua service berstatus healthy/running.
5. Example DAG terdeteksi dan dapat dijalankan.
6. Upload ke GCS muncul di VM dalam waktu sekitar dua menit.
7. VM yang direstart menjalankan kembali Airflow dan timer secara otomatis.

## 8. Provisioning aktual

Script `scripts/bootstrap_debian_vm.sh` mengotomasi instalasi Docker Engine, Docker Compose, Google Cloud CLI, user service, secret lokal, build image, migrasi database, dan aktivasi systemd pada VM Debian.

## 9. Menambahkan dbt dan dataset per student

- Menambahkan `dbt-bigquery` versi `1.12.0` pada virtual environment terpisah di `/home/airflow/dbt-venv` agar dependensinya tidak berbenturan dengan provider Google Airflow.
- Menambahkan panduan struktur project, `profiles.yml`, autentikasi ADC, dan contoh DAG yang menjalankan `dbt build`.
- Memberikan `roles/bigquery.user` kepada service account VM agar DAG dapat membuat dataset `cp3_<student_id>`.
- Menguji izin dengan membuat lalu menghapus dataset sementara `cp3_permission_test`.
- Build memerlukan akses PyPI. Pada deployment tanpa Cloud NAT, external IP dipasang sementara selama build dan langsung dilepas kembali; firewall ingress tetap hanya mengizinkan SSH dari IAP.
