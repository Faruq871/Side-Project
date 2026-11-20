{{ config(materialized='table') }}

select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchased_at,
    o.delivered_to_customer_at,
    o.estimated_delivery_at,
    v.item_count,
    v.merchandise_value,
    v.freight_value,
    v.total_order_value,
    case
        when o.delivered_to_customer_at is null then null
        when o.delivered_to_customer_at > o.estimated_delivery_at then true
        else false
    end as is_delivered_late
from {{ ref('stg_orders') }} as o
left join {{ ref('int_order_value') }} as v using (order_id)
