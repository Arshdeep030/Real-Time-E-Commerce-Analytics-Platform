CREATE TABLE IF NOT EXISTS fact_user_sessions (
    user_id        VARCHAR,
    session_start  TIMESTAMP,
    session_end    TIMESTAMP,
    event_count    INT,
    total_amount   FLOAT
);

INSERT INTO fact_user_sessions
SELECT
    custid AS user_id,
    session_start,
    session_end,
    purchase_count AS event_count,
    total_amount
FROM sessionized_events s
WHERE NOT EXISTS (
    SELECT 1
    FROM fact_user_sessions f
    WHERE f.user_id = s.custid
      AND f.session_start = s.session_start
);
