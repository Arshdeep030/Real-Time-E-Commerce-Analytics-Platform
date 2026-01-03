SELECT 
    SUM(total_sessions) as total_traffic,
    SUM(total_purchases) as total_sales,
    ROUND((SUM(total_purchases)::float / SUM(total_sessions)) * 100, 2) as conversion_rate
FROM analytics.fct_conversion_funnel;