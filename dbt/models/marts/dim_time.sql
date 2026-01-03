SELECT DISTINCT
    window_start AS timestamp,
    EXTRACT(hour FROM window_start) AS hour,
    EXTRACT(day FROM window_start) AS day,
    EXTRACT(month FROM window_start) AS month,
    EXTRACT(year FROM window_start) AS year
FROM {{ ref('fact_user_sessions') }}
