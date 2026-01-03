
-- COPY Sessionized Events from S3 to Redshift
-- Set AWS credentials in Redshift (or use IAM role)
-- Example with IAM Role attached to Redshift cluster
COPY stg_sessionized_events(user_id, window_start, window_end, event_count)
FROM 's3://ecommerce-enriched/sessionized/'
IAM_ROLE 'arn:aws:iam::478867930203:role/RedshiftS3AccessRole'
FORMAT AS PARQUET
TIMEFORMAT 'auto'
COMPUPDATE ON
STATUPDATE ON;
