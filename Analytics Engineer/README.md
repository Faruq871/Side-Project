# Olist dbt Transformation

## Overview
This project transforms raw Olist e-commerce data into an analytics-ready star schema using dbt (data build tool). It ingests 9 tables from the `raw` schema, applies data quality tests, calculates business metrics, and generates comprehensive documentation.

## Objectives
- **Build a Star Schema:** Structure data into standardized dimension and fact tables for efficient analytical querying.
- **Ensure Data Quality:** Implement automated testing (generic and custom) to validate primary keys, referential integrity, and business logic.
- **Calculate Business Metrics:** Derive actionable insights such as delivery delays and seller monthly revenue.
- **Auto-Generate Documentation:** Produce a navigable data dictionary and lineage graph via dbt docs.

## Star Schema & Grain Definition

### Dimension Tables
| Table Name | Grain (1 row = ...) | Description |
|------------|---------------------|-------------|
| `dim_customers` | 1 customer record (`customer_id`) | Customer demographic and location data. |
| `dim_products` | 1 product (`product_id`) | Product attributes and category translations. |
| `dim_sellers` | 1 seller (`seller_id`) | Seller location data. |
| `dim_date` | 1 calendar day (`date_day`) | Date spine from 2016-01-01 to 2018-12-31. |

### Fact Tables
| Table Name | Grain (1 row = ...) | Description |
|------------|---------------------|-------------|
| `fct_order_items` | 1 line item within an order (`order_id` + `order_item_id`) | Granular transaction details, including price, freight, and delivery metrics. |
| `fct_orders` | 1 order (`order_id`) | Aggregated order-level data, including total revenue, total freight, and item count. |

## Business Metrics
1. **Delivery Delay (`delivery_delay_days`)**: Calculated in `fct_order_items` as the difference in days between `order_delivered_customer_date` and `order_estimated_delivery_date`. Positive values indicate late delivery.
2. **Seller Monthly Revenue (`seller_monthly_revenue`)**: Calculated in `fct_order_items` using a window function: `SUM(price) OVER (PARTITION BY seller_id, DATE_TRUNC('month', order_purchase_timestamp))`.

## Prerequisites
1. PostgreSQL database running with the `raw` schema populated (from Task No. 2).
2. Python environment with dbt installed:
   ```bash
   pip install dbt-core dbt-postgres
   ```
3. A `profiles.yml` file configured outside the repository (e.g., `~/.dbt/profiles.yml` on Linux/Mac or `%USERPROFILE%\.dbt\profiles.yml` on Windows):
   ```yaml
   olist_dbt:
     target: dev
     outputs:
       dev:
         type: postgres
         host: localhost
         user: olist
         password: "{{ env_var('POSTGRES_PASSWORD', 'olist_secret') }}"
         port: 5432
         dbname: olist
         schema: public
         threads: 4
   ```

## Usage

### 1. Verify Connection
```bash
dbt debug
```
*Expected output: `Connection test: OK`*

### 2. Build Models and Run Tests
```bash
dbt build
```
*This executes all models (views for staging, tables for marts) and runs all defined tests. It must complete with 0 errors.*

### 3. Generate Documentation
```bash
dbt docs generate
```
*Creates HTML documentation files in the `target/` directory.*

### 4. View Documentation Locally (Optional)
```bash
dbt docs serve
```
*Opens the documentation in your default web browser (usually at `http://localhost:8080`).*

### 5. Host Documentation on GitHub Pages
```bash
git checkout -b gh-pages
cp -r target/* .
git add .
git commit -m "chore: update dbt docs"
git push origin gh-pages
```
*After pushing, enable GitHub Pages in the repository settings, setting the source to the `gh-pages` branch.*

## Project Structure
```text
olist-dbt-transformation/
├── dbt_project.yml           # Project configuration
├── models/
│   ├── staging/              # 1:1 mapping and cleaning of raw tables
│   ├── marts/                # Star schema (dimensions and facts)
│   └── schema.yml            # Model descriptions and test definitions
├── macros/                   # Custom data quality tests
└── README.md                 # Project documentation
```

## Verification (Definition of Done)
- `dbt build` completes successfully with 0 errors and 0 warnings.
- All generic and custom tests pass.
- Running `dbt build` a second time yields identical row counts in `fct_orders` and `fct_order_items`, proving idempotency.
- dbt documentation is successfully hosted and accessible via GitHub Pages.
```