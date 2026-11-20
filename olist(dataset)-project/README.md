# Olist Dataset Project

Working with the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

## Tools

- PostgreSQL, SQL
- Python, Pandas, NumPy
- Docker, Apache Airflow
- dbt, Jinja
- Jupyter, Matplotlib, Seaborn
- Scikit-learn, TensorFlow/Keras

## Files

```text
olist-dataset-project/
├── airflow/dags/          # Airflow workflows
├── data/raw/              # Original CSV files
├── data/processed/        # Prepared data
├── dbt/olist/             # dbt project
├── docs/                  # Project notes
├── notebooks/analysis/    # Data exploration
├── notebooks/prediction/  # Prediction work
├── notebooks/modeling/    # Model experiments
├── reports/               # Charts and results
├── sql/schema.sql         # Database schema
├── src/ingestion/         # CSV loading scripts
├── tests/                 # Tests
├── .env.example
├── docker-compose.yml
└── requirements.txt
```

## Dataset

1. Download the dataset from Kaggle.
2. Extract the CSV files into `data/raw/`.
3. Keep the original filenames. Do not commit the dataset to Git.

Required files:

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

## Run

```bash
cp .env.example .env
docker compose up -d postgres
python -m src.ingestion.load_olist --data-dir data/raw
```

Run dbt:

```bash
cd dbt/olist
dbt debug && dbt run && dbt test
```

Start Airflow:

```bash
docker compose up -d airflow
```

Airflow UI: http://localhost:8080

## What to Work On

| Part | Tasks |
|---|---|
| SQL | Create tables, keys, constraints, and queries |
| Ingestion | Load CSV files into PostgreSQL |
| Airflow | Schedule the data loading and dbt jobs |
| dbt | Clean, join, and prepare tables |
| Analysis | Study orders, customers, sellers, products, and deliveries |
| Prediction | Build and check predictive models |
| Modeling | Train and evaluate machine learning models |

## Questions

- How do order numbers change over time?
- Which products and sellers have the highest sales?
- What is linked to late deliveries?
- Do delivery times relate to review scores?
- Can late deliveries or review scores be predicted?

## Notes

- Leave the original files unchanged in `data/raw/`.
- An order can have multiple items, payments, and reviews. Aggregate these tables before joining them to order-level data.
- Check for target leakage before training a model.
- Do not commit passwords, keys, or raw dataset files.
- Follow the dataset's original license and terms.
