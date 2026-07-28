# Contoh submission dengan dbt

DAG `example_with_dbt_pipeline.py` menunjukkan pola minimum:

1. Membuat dataset `cp3_example_with_dbt` di `asia-southeast2`.
2. Menjalankan `dbt build` memakai service account VM melalui Application Default Credentials.
3. Menulis artefak `target/` dan log dbt ke `/tmp`, karena folder DAG di-mount read-only.
4. Membuat model staging, data mart terpartisi/ter-cluster, dan data test.

Student harus mengganti `STUDENT_ID`, `dag_id`, nama project/profile dbt, sumber data, model, dan test. Jangan menambahkan `keyfile` atau JSON service-account key.
