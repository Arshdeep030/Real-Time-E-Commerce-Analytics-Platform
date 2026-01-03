{{ config(materialized='table') }}

SELECT
    window_start::date as activity_date,
    -- Use 'event_count' because that is the alias you created in staging
    COUNT(DISTINCT session_id) as total_sessions,
    SUM(CASE WHEN event_count > 0 THEN 1 ELSE 0 END) as total_purchases,
    SUM(total_amount) as total_revenue
FROM {{ ref('stg_sessionized_events') }}
GROUP BY 1