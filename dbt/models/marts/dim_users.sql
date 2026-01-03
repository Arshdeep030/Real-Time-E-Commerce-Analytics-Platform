SELECT DISTINCT
    user_id
FROM {{ ref('fact_user_sessions') }}
