from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, col
from pyspark.sql.types import TimestampType

spark = SparkSession.builder \
    .appName("EcommerceDailyBatch") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read raw events from S3 or local parquet
df = spark.read.parquet("s3://ecommerce-data/curated/events/")  

# Cast event_time
df = df.withColumn("event_time", col("event_time").cast(TimestampType()))

# Daily revenue and number of purchases
daily_metrics = df.filter(col("event_type") == "purchase") \
    .groupBy(col("event_time").cast("date").alias("date")) \
    .agg(
        sum("price").alias("daily_revenue"),
        count("event_id").alias("total_purchases")
    )

daily_metrics.show()
