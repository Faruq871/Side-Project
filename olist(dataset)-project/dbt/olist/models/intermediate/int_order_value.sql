{{ config(materialized='view') }}

select
    order_id,
    count(*) as item_count,
    sum(item_price) as merchandise_value,
    sum(freight_value) as freight_value,
    sum(item_price + freight_value) as total_order_value
from {{ ref('stg_order_items') }}
group by order_id
