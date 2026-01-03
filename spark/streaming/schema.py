from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

event_schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("device", StringType(), True),
    StructField("country", StringType(), True)
])
