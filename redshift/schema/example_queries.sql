-- Count sessions per user
SELECT user_id, COUNT(*) AS total_sessions
FROM fact_sessions
GROUP BY user_id
ORDER BY total_sessions DESC;

-- Average events per session
SELECT AVG(event_count) AS avg_events_per_session
FROM fact_sessions;

-- Join session fact with user dimension
SELECT f.user_id, u.first_seen, SUM(f.event_count) AS total_events
FROM fact_sessions f
JOIN dim_users u
ON f.user_id = u.user_id
GROUP BY f.user_id, u.first_seen;
