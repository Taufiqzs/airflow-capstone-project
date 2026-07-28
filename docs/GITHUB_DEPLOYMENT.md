# Deployment DAG dari GitHub

Contoh workflow berada di `examples/github-actions/deploy-dags.yml`. Salin ke `.github/workflows/deploy-dags.yml` pada repository deployment.

## Alur

1. Student membuat branch dan pull request.
2. Instruktur memeriksa Python, credential, dan dampak task.
3. Setelah merge ke `main`, GitHub-hosted runner menjalankan validator.
4. GitHub melakukan autentikasi ke GCP dengan OIDC Workload Identity Federation.
5. Folder `dags/submissions` disinkronkan ke bucket GCS.
6. VM mengambil perubahan melalui timer.

## Variable GitHub Environment

Buat environment `cp3-production`, lalu tambahkan variable:

- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_DEPLOY_SERVICE_ACCOUNT`
- `CP3_DAG_BUCKET` tanpa prefix `gs://`

Service account deployment hanya memerlukan izin menulis dan menghapus object pada bucket DAG. Jangan memberikan role project Editor atau Owner.

Aktifkan required reviewer pada environment jika tersedia. Workflow hanya berjalan pada push ke `main`, bukan langsung dari event pull request.

## Mengapa tidak memakai self-hosted runner

DAG adalah Python yang dapat dieksekusi. Persistent self-hosted runner pada VM yang sama akan memperbesar dampak bila workflow atau submission berbahaya. GitHub-hosted runner + GCS juga tetap dapat deploy saat Spot VM sedang offline.

