CREATE TABLE IF NOT EXISTS dim_users (
    user_id VARCHAR PRIMARY KEY
);

INSERT INTO dim_users
SELECT DISTINCT custid
FROM sessionized_events
WHERE custid NOT IN (
    SELECT user_id FROM dim_users
);
