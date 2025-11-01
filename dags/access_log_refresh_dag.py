from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_sqlalchemy_loader():
    from sqlalchemy import create_engine, text
    import pandas as pd
    import os

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "access_log_analysis")

    CSV_PATH = "/opt/airflow/data/access_logs.csv"

    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS access_logs (
        log_id SERIAL PRIMARY KEY,
        user_id INT,
        username VARCHAR(50),
        login_time TIMESTAMP,
        logout_time TIMESTAMP,
        ip_address VARCHAR(50),
        device_type VARCHAR(20),
        status VARCHAR(20),
        branch_name VARCHAR(50),
        role VARCHAR(50)
    );
    """

    # ✅ Ensure table exists
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))
        print("✅ Table created or already exists.")

    # ✅ Read CSV
    if not os.path.exists(CSV_PATH):
        print(f"❌ CSV not found at {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    print(f"📄 CSV loaded with {len(df)} rows.")

    # ✅ Remove records that already exist
    with engine.connect() as conn:
        existing_ids = pd.read_sql("SELECT log_id FROM access_logs", conn)
        before_count = len(df)

        df = df[~df["log_id"].isin(existing_ids["log_id"])]
        after_count = len(df)

        if after_count == 0:
            print("⚠️ No new rows to insert — skipping append.")
        else:
            df.to_sql("access_logs", engine, if_exists="append", index=False)
            print(f"✅ Inserted {after_count} new rows (skipped {before_count - after_count}).")

    print("🎯 ETL with SQLAlchemy + Docker completed successfully.")


with DAG(
    dag_id="access_log_refresh_dag",
    default_args=default_args,
    description="Automated ETL pipeline using Airflow + dbt + SQLAlchemy",
    schedule="@daily",
    start_date=datetime(2025, 11, 1),
    catchup=False,
) as dag:

    load_task = PythonOperator(
        task_id="load_access_logs",
        python_callable=run_sqlalchemy_loader,
    )

    dbt_run = BashOperator(
        task_id="run_dbt_models",
        bash_command='dbt run --project-dir /home/airflow/dbt_projects/access_log_project --profiles-dir /home/airflow/.dbt',
        dag=dag,
    )

load_task >> dbt_run
