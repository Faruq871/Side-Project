import os
import pandas as pd
from sqlalchemy import create_engine, text
from airflow.decorators import dag, task
from datetime import datetime

DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
DB_HOST = 'postgres'
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

DATA_DIR = '/opt/airflow/data'
CHUNK_SIZE = 50000

TABLE_MAPPING = {
    'customers': 'customers',
    'geolocation': 'geolocation',
    'order_items': 'order_items',
    'order_payments': 'order_payments',
    'order_reviews': 'order_reviews',
    'orders': 'orders',
    'products': 'products',
    'sellers': 'sellers',
    'product_category_name_translation': 'product_category_name_translation'
}

@dag(
    dag_id='olist_etl_pipeline',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['olist', 'etl'],
    default_args={'retries': 2, 'retry_delay': 60}
)
def olist_etl_pipeline():

    @task
    def get_file_list():
        return list(TABLE_MAPPING.keys())

    @task
    def extract_and_load(file_base: str):
        table_name = TABLE_MAPPING[file_base]
        csv_path = os.path.join(DATA_DIR, f"{file_base}.csv")
        engine = create_engine(DB_URL)
        
        # Idempotency: Clear table before loading
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE raw.{table_name} RESTART IDENTITY;"))
            conn.commit()

        row_count = 0
        for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE, dtype=str):
            date_cols = [col for col in chunk.columns if 'timestamp' in col or 'date' in col]
            for col in date_cols:
                chunk[col] = pd.to_datetime(chunk[col], errors='coerce')
                
            chunk.to_sql(
                name=table_name, con=engine, schema='raw',
                if_exists='append', index=False, chunksize=10000
            )
            row_count += len(chunk)
            
        return {table_name: row_count}

    @task
    def validate_counts(loaded_counts: list):
        engine = create_engine(DB_URL)
        errors = []
        
        for count_dict in loaded_counts:
            for table_name, csv_count in count_dict.items():
                with engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM raw.{table_name};"))
                    db_count = result.scalar()
                    
                if csv_count != db_count:
                    errors.append(f"Mismatch in {table_name}: CSV={csv_count}, DB={db_count}")
                    
        if errors:
            raise ValueError("Validation failed:\n" + "\n".join(errors))
            
        print("All row counts match. Validation successful.")

    file_list = get_file_list()
    loaded_counts = extract_and_load.expand(file_base=file_list)
    validate_counts(loaded_counts)

olist_etl_pipeline()