# Contoh submission tanpa dbt

DAG `example_without_dbt_pipeline.py` menunjukkan pola minimum:

1. Membuat dataset `cp3_example_without_dbt` di `asia-southeast2` secara idempotent.
2. Menjalankan transformasi SQL langsung melalui BigQuery.
3. Membuat tabel yang dipartisi dan di-cluster.
4. Menjalankan quality check dengan BigQuery `ASSERT`.

Student harus mengganti `STUDENT_ID`, `dag_id`, sumber data, transformasi, dan quality check sesuai project masing-masing.
