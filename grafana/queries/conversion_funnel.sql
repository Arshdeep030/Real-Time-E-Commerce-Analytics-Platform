SELECT 
    SUM(total_sessions) AS sessions, 
    SUM(total_purchases) AS purchases, 
    SUM(total_revenue) AS revenue 
FROM analytics.fct_conversion_funnel;