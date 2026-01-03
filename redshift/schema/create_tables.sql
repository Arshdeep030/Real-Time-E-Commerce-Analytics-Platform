
CREATE TABLE IF NOT EXISTS stg_sessionized_events (
    user_id VARCHAR(50),
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    event_count INT
);


CREATE TABLE IF NOT EXISTS fact_sessions (
    session_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    event_count INT NOT NULL
);


CREATE TABLE IF NOT EXISTS dim_users (
    user_id VARCHAR(50) PRIMARY KEY,
    first_seen TIMESTAMP DEFAULT GETDATE()
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100)
);
