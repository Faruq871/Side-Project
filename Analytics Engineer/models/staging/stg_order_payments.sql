select 
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value::numeric
from {{ source('olist_raw', 'order_payments') }}