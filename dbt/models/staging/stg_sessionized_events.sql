SELECT
    custid AS user_id,
    session_id,
    session_start AS window_start,
    session_end AS window_end,
    purchase_count AS event_count,
    total_amount
FROM sessionized_events
