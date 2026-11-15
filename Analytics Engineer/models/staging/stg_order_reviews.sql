select 
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date::timestamp,
    review_answer_timestamp::timestamp
from {{ source('olist_raw', 'order_reviews') }}