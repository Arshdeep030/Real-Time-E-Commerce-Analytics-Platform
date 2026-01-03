SELECT
    'Total Sessions' as metric,
    SUM(total_sessions) as value
FROM analytics.fct_conversion_funnel
UNION ALL
SELECT
    'Successful Purchases',
    SUM(total_purchases)
FROM analytics.fct_conversion_funnel