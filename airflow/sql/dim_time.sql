CREATE TABLE IF NOT EXISTS dim_time (
    date  DATE PRIMARY KEY,
    year  INT,
    month INT,
    day   INT
);

INSERT INTO dim_time
SELECT DISTINCT
    DATE(session_start),
    EXTRACT(year FROM session_start),
    EXTRACT(month FROM session_start),
    EXTRACT(day FROM session_start)
FROM sessionized_events
WHERE DATE(session_start) NOT IN (
    SELECT date FROM dim_time
);
