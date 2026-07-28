# Deployment DAG dari GitHub

Workflow aktif berada di `.github/workflows/deploy-dags.yml`. Contoh asal tetap tersedia di `examples/github-actions/deploy-dags.yml`.

## Alur

1. Student membuat branch dan pull request.
2. Instruktur memeriksa Python, credential, dan dampak task.
3. Pada pull request, GitHub-hosted runner menjalankan validator tanpa mengakses GCP.
4. Setelah merge ke `main`, validator dijalankan kembali dan job deployment dimulai.
5. GitHub melakukan autentikasi ke GCP dengan OIDC Workload Identity Federation.
6. Folder `dags/submissions` disinkronkan ke bucket GCS.
7. VM mengambil perubahan melalui timer.

## Konfigurasi deployment saat ini

Workflow sudah dikonfigurasi untuk:

- Repository `riodpp/airflow-capstone-project`.
- Workload Identity Provider `projects/187742136599/locations/global/workloadIdentityPools/cp3-github/providers/github`.
- Service account `cp3-github-deployer@jcdeah-009.iam.gserviceaccount.com`.
- Bucket `gs://jcdeah-009-cp3-airflow-dags`.

Nilai tersebut bukan credential dan boleh disimpan di workflow. Tidak ada JSON key atau secret GCP pada GitHub. Service account deployment hanya memiliki `roles/storage.objectAdmin` pada bucket DAG dan tidak memiliki role project Editor atau Owner.

Jika diperlukan approval tambahan, buat GitHub Environment lalu tambahkan `environment` pada job `deploy`. Workflow saat ini hanya melakukan deployment dari branch `main`; pull request hanya menjalankan validasi.

## Mengapa tidak memakai self-hosted runner

DAG adalah Python yang dapat dieksekusi. Persistent self-hosted runner pada VM yang sama akan memperbesar dampak bila workflow atau submission berbahaya. GitHub-hosted runner + GCS juga tetap dapat deploy saat Spot VM sedang offline.
