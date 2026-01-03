from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, TimestampType, DoubleType


#  Spark Session
spark = SparkSession.builder \
    .appName("EcommerceSessionization") \
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

json_df = df.select(
    from_json(col("value").cast("string"), event_schema).alias("data")
).select("data.*")


#  Sessionization 
session_df = json_df.groupBy(
    col("user_id"),
    window(col("event_time"), "30 minutes")
).count()

#  Write to Kafka Enriched Topic
kafka_query = session_df.selectExpr(
    "to_json(struct(*)) AS value"
).writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "ecommerce_events_enriched") \
    .option("checkpointLocation", "/tmp/spark_checkpoint_kafka") \
    .outputMode("update") \
    .start()


local_query = session_df.writeStream \
    .format("parquet") \
    .option("path", "/tmp/sessionized_output/") \
    .option("checkpointLocation", "/tmp/spark_checkpoint_local") \
    .outputMode("append") \
    .start()


spark.streams.awaitAnyTermination()
