# Olist ETL Pipeline

## Overview
This project automates the extraction of 9 Olist CSV files and loads them into a PostgreSQL database using Apache Airflow. The pipeline is designed to be idempotent, repeatable, and resilient to failures.

## Architecture & Idempotency Decision

### Load Strategy: `TRUNCATE + INSERT` (Full Refresh)
**Reason:** The Olist dataset is a static historical snapshot. `TRUNCATE` ensures a clean state before each load, and `INSERT` guarantees the data is 100% identical to the source without the complexity of `UPSERT` logic.

**Trade-offs:**
- **Pros:** Simple logic, fast execution, guarantees data consistency with source.
- **Cons:** Table locks during the load operation. This is acceptable because no concurrent processes read the `raw` tables directly.

### Geolocation Handling
`raw.geolocation` has no Primary Key. The `raw` layer must be an exact 1:1 mirror of the source. Deduplication of geolocation data will be handled in the Staging layer using dbt (Task No. 3).

## Proof of Idempotency (DoD)

The DAG was triggered twice in succession. Both runs completed successfully. Row counts remained identical across both runs, confirming idempotency:

| Table Name | Row Count |
|------------|-----------|
| customers | 99,441 |
| geolocation | 1,001,631 |
| sellers | 3,095 |
| products | 32,951 |
| orders | 99,441 |
| order_items | 112,650 |
| order_payments | 103,886 |
| order_reviews | 68,065 |
| product_category_name_translation | 71 |

## How to Run
1. Place the 9 Olist CSV files in the `data/` folder.
2. Run `docker compose up -d`.
3. Access Airflow UI at `http://localhost:8080` (admin/admin_secret).
4. Trigger the `olist_etl_pipeline` DAG.
```
