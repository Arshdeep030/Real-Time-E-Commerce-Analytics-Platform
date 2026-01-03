{{ config(materialized='incremental', unique_key='user_id || window_start') }}

SELECT
    user_id,
    window_start,
    window_end,
    event_count,
    total_amount
FROM {{ ref('stg_sessionized_events') }}

{% if is_incremental() %}
WHERE window_start > (SELECT MAX(window_start) FROM {{ this }})
{% endif %}
