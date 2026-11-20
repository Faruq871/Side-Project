# Project Notes

## Scope

Explore Olist orders, sales, delivery performance, customer reviews, products, and sellers.

## Data Layers

- **Raw:** source tables with original column names.
- **Staging:** data types and basic cleanup.
- **Intermediate:** reusable joins and calculations.
- **Marts:** tables prepared for analysis and reporting.

## Metrics

- **Item value:** sum of item prices, excluding freight.
- **Freight value:** sum of shipping charges.
- **Order value:** item value plus freight value.
- **Late delivery:** delivered timestamp later than the estimated delivery timestamp. Undelivered orders remain unclassified.

## Data Checks

- Geolocation may contain multiple records per ZIP-code prefix.
- An order may have multiple reviews, items, and payments.
- Aggregate child tables to order level before joining to avoid duplicate totals.
- Predictive features must only use information available at prediction time.
