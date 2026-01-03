-- Query for Active Users & Events Summary
SELECT
  window_start AS time,
  COUNT(DISTINCT user_id) AS active_users,
  SUM(event_count) AS total_events
FROM analytics.fact_user_sessions
GROUP BY 1
ORDER BY 1;