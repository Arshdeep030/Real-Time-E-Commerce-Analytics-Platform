SELECT 
    date_trunc('day', window_start) as day,
    SUM(total_amount) as daily_revenue,
    LAG(SUM(total_amount)) OVER (ORDER BY date_trunc('day', window_start)) as prev_day_revenue
FROM analytics.fact_user_sessions
GROUP BY 1
ORDER BY 1;