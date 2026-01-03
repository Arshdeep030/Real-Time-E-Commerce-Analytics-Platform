from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, struct, to_json
from pyspark.sql.types import StructType, StringType, TimestampType, DoubleType
import os

#  Spark Session with AWS S3
spark = SparkSession.builder \
    .appName("EcommerceSessionization") \
    .config("spark.sql.streaming.statefulOperator.checkConsistency", "false") \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", "*******************") \
    .config("spark.hadoop.fs.s3a.secret.key", "***********************************") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

#  Event Schema
event_schema = StructType() \
    .add("user_id", StringType()) \
    .add("event_type", StringType()) \
    .add("product_id", StringType()) \
    .add("price", DoubleType()) \
    .add("event_time", TimestampType())

#  Read Kafka Raw Events
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ecommerce_events_raw") \
    .option("startingOffsets", "latest") \
    .load()

json_df = df.select(from_json(col("value").cast("string"), event_schema).alias("data")) \
            .select("data.*")

#  Sessionization
session_df = json_df.withWatermark("event_time", "1 minute") \
    .groupBy(
        col("user_id"),
        window(col("event_time"), "1 minute")
    ).count()

#  Write to Kafka (Enriched)
kafka_checkpoint = "/tmp/checkpoints/kafka_v2"
kafka_query = session_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "ecommerce_events_enriched") \
    .option("checkpointLocation", kafka_checkpoint) \
    .outputMode("update") \
    .start()

#  Write to AWS S3 (Parquet)
s3_checkpoint = "s3a://ecommerce-enriched/checkpoints/v2"
s3_query = session_df.writeStream \
    .format("parquet") \
    .option("path", "s3a://ecommerce-enriched/sessionized/") \
    .option("checkpointLocation", s3_checkpoint) \
    .outputMode("append") \
    .start()

#  Keep Streaming Alive
spark.streams.awaitAnyTermination()