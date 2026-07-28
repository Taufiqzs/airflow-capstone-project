# Panduan Student

## Lokasi file

```text
dags/submissions/<student_id>/<student_id>_<pipeline>.py
```

## Aturan DAG

- `dag_id` wajib unik, lowercase, dan diawali student ID.
- Gunakan `catchup=False` kecuali memang dibutuhkan dan dijelaskan.
- Gunakan maksimum satu active run dan hindari dynamic task mapping tanpa batas.
- Jangan menyimpan credential, service-account key, token, atau password dalam DAG.
- Gunakan Airflow Connection atau autentikasi service account VM yang sudah disetujui instruktur.
- Jangan melakukan pemrosesan Spark/Pandas besar pada VM Airflow. Submit job ke Dataflow, Dataproc, BigQuery, atau layanan setara.
- Setiap task harus idempotent atau menjelaskan strategi rerun.
- Hindari proses tanpa batas, server, publisher streaming permanen, dan infinite loop di dalam task Airflow.
- Publisher streaming sebaiknya dijalankan sebagai cloud job/container dengan durasi atau jumlah event yang terkontrol.

## Dataset BigQuery student

- Student boleh membuat dataset baru dengan nama `cp3_<student_id>`; gunakan lowercase dan underscore saja.
- Lokasi dataset harus sama dengan data sumber dan tabel lain yang akan di-query bersama.
- DAG boleh membuat dataset secara idempotent (`exists_ok=True`) sebelum menjalankan transformasi.
- Jangan membaca, mengubah, atau menghapus dataset student lain. Semua DAG pada instalasi ini memakai service account VM yang sama, sehingga aturan nama dan proses review menjadi batas operasional utama.
- Sertakan lokasi, tujuan dataset, tabel yang dibuat, serta langkah cleanup di README submission.
- Contoh pembuatan dataset dan penggunaan dbt tersedia di [DBT_USAGE.md](DBT_USAGE.md).

## Jika menggunakan dbt

- Simpan project di `dags/submissions/<student_id>/dbt/` bersama `dbt_project.yml`, folder `models/`, dan test.
- Jalankan `dbt build`, bukan hanya `dbt run`, agar model dan data test dieksekusi.
- Gunakan autentikasi bawaan VM (`method: oauth`); jangan mengunggah file key service account.
- Batasi `threads` maksimal 2 dan gunakan model incremental untuk transformasi besar bila sesuai.
- Nama dataset target tetap `cp3_<student_id>` dan nama model harus tidak bertabrakan dengan student lain.

## Sebelum pull request

1. Jalankan `python3 scripts/validate_dags.py dags/submissions`.
2. Pastikan tidak ada secret pada commit.
3. Sertakan penjelasan schedule, connection yang dibutuhkan, resource cloud, estimasi durasi, dan cara menghentikan resource.
4. DAG akan masuk dalam kondisi paused. Instruktur yang mengaktifkan setelah review.
