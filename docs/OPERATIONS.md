# Operasi dan Recovery

## Pemeriksaan rutin

```bash
docker compose ps
docker compose logs --tail=200 airflow-scheduler airflow-dag-processor
systemctl status cp3-dag-sync.timer
journalctl -u cp3-dag-sync.service --since today
df -h
```

## Update project

1. Backup metadata database.
2. Pull/copy perubahan terverifikasi.
3. Build image baru.
4. Jalankan migrasi dengan `docker compose up airflow-init`.
5. Restart service Airflow dan periksa health check.

## Rotasi password admin Simple Auth

Jalankan `sudo python3 /opt/cp3-airflow/scripts/rotate_simple_auth_password.py`, lalu restart API server. Ambil password baru langsung melalui SSH dari file yang disebutkan script; jangan menyalinnya ke repository atau log publik.

## Backup metadata

Database metadata menyimpan user, connection, variable, dan riwayat run. Lakukan `pg_dump` berkala ke bucket terpisah dengan retention terbatas. Jangan menyimpan dump di repository atau bucket DAG student.

## Disk penuh

- Bersihkan log lama menggunakan retention yang terkontrol.
- Jangan menghapus Docker volume PostgreSQL tanpa backup.
- Jangan menyimpan dataset student pada boot disk Airflow.

## DAG tidak muncul

1. Jalankan validator.
2. Periksa log `cp3-dag-sync.service`.
3. Periksa log DAG processor.
4. Pastikan file berada di `dags/submissions` dan memiliki ekstensi `.py`.

## Spot VM berhenti

Tidak ada job baru yang dijadwalkan saat VM berhenti. Job cloud yang sudah disubmit dapat terus berjalan tergantung layanannya. Setelah VM hidup, systemd memulai Airflow dan menyinkronkan DAG terbaru. Periksa state task sebelum melakukan rerun.
