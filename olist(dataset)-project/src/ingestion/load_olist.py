"""Load the Olist CSV source files into PostgreSQL raw tables."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

FILE_TABLE_MAP = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation",
}


def database_url() -> str:
    load_dotenv()
    user = os.getenv("POSTGRES_USER", "olist")
    password = os.getenv("POSTGRES_PASSWORD", "olist_dev_password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "olist_dw")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"


def load_file(path: Path, table: str, engine) -> int:
    if not path.is_file():
        raise FileNotFoundError(f"Required dataset file not found: {path}")
    frame = pd.read_csv(path)
    # Keep the pre-created PostgreSQL schema and constraints intact.
    with engine.begin() as connection:
        connection.execute(text(f'TRUNCATE TABLE raw."{table}"'))
    frame.to_sql(table, engine, schema="raw", if_exists="append", index=False,
                 chunksize=10_000, method="multi")
    return len(frame)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    engine = create_engine(database_url(), pool_pre_ping=True)
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    for filename, table in FILE_TABLE_MAP.items():
        count = load_file(args.data_dir / filename, table, engine)
        print(f"Loaded {count:,} rows into raw.{table}")
    engine.dispose()


if __name__ == "__main__":
    main()
