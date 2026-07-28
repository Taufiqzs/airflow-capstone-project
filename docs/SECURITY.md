# Keamanan Minimum

DAG Airflow adalah kode Python yang dieksekusi pada host. Validator dalam project ini hanya memeriksa syntax, ukuran file, dan keunikan ID; validator bukan sandbox keamanan.

## Wajib

- Hanya merge submission yang sudah direview manusia.
- Gunakan repository private bila memungkinkan.
- Jangan menjalankan deployment VM dari pull request yang belum dipercaya.
- Gunakan Workload Identity Federation, bukan JSON service-account key.
- Terapkan least privilege pada service account VM dan service account deployment.
- Pisahkan bucket DAG dari bucket backup atau data siswa.
- Simpan UI pada localhost dan akses melalui IAP/SSH tunnel.
- Ganti seluruh password dan key contoh.
- Jangan memasukkan Docker socket ke container Airflow.
- Jangan memberi student akses shell ke VM.

## Batas isolasi

Semua DAG berbagi host, Python environment, metadata database, dan identitas cloud Airflow. Ini cocok untuk kelas dengan submission terpercaya dan review ketat, tetapi bukan multi-tenant isolation. Untuk kode yang tidak dipercaya, gunakan project GCP atau runtime terpisah per student dan biarkan Airflow hanya memanggil API job tersebut.

