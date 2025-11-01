from sqlalchemy import create_engine, text
import pandas as pd
import os

DB_USER = os.getenv("DB_USER", "airflow")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "access_log_analysis")


CSV_PATH = "/data/access_logs.csv"

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

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    print("✅ Table created or exists.")

if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    df.to_sql("access_logs", engine, if_exists="append", index=False)
    print(f"✅ Loaded {len(df)} rows into PostgreSQL.")
else:
    print(f"❌ CSV not found at {CSV_PATH}")

print("🎯 ETL with SQLAlchemy + Docker completed.")
