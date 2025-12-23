from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/app')

from straming_pipeline_docker import create_table, stream_batch

with DAG(
    dag_id="aerostream_streaming",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/1 * * * *",
    catchup=False,
    tags=["streaming", "nlp"]
) as dag:

    init_db = PythonOperator(
        task_id="init_db",
        python_callable=create_table
    )

    fetch_and_predict = PythonOperator(
        task_id="fetch_and_predict",
        python_callable=stream_batch,
        op_kwargs={"batch_size": 10}
    )

    init_db >> fetch_and_predict