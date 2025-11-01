# Use official Apache Airflow base image
FROM apache/airflow:2.9.3

# Switch to root to install system dependencies
USER root

# Install git and clean up to reduce image size
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install all required Python packages under airflow user
RUN pip install --no-cache-dir \
    "dbt-core==1.9.0" \
    "dbt-postgres==1.9.0" \
    "requests" \
    "pandas" \
    "faker" \
    "sqlalchemy" \
    "psycopg2-binary"
