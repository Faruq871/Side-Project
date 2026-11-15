{% test valid_order_status(model, column_name) %}
select {{ column_name }} from {{ model }}
where {{ column_name }} not in ('created', 'approved', 'in_process', 'shipped', 'delivered', 'canceled', 'unavailable')
{% endtest %}