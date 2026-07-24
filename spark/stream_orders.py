from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *


spark = (
    SparkSession.builder
    .appName("NovaCart")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Schema matching the producer
schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("amount", IntegerType(), True),
    StructField("status", StringType(), True),
    StructField("payment_status", StringType(), True),
    StructField("timestamp", StringType(), True),
])

# Read stream from Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "orders")
    .option("startingOffsets", "latest")
    .load()
)

# Parse JSON messages
parsed_df = (
    df.selectExpr("CAST(value AS STRING)")
      .select(from_json(col("value"), schema).alias("data"))
      .select("data.*")
)

valid_orders = parsed_df.filter(
    col("order_id").isNotNull() &
    col("customer_id").isNotNull() &
    (col("customer_id") > 0) &
    col("product").isNotNull() &
    (col("product") != "") &
    col("product").isin(VALID_PRODUCTS) &
    col("quantity").isNotNull() &
    (col("quantity") > 0) &
    col("amount").isNotNull() &
    (col("amount") > 0) &
    (col("amount") < 1000000) &
    col("status").isin(
        "PLACED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED"
    ) &
    col("payment_status").isin(
        "PAID",
        "PENDING",
        "REFUNDED"
    ) &
    ~(
        (col("status") == "CANCELLED") &
        (col("payment_status") == "PAID")
    ) &
    ~(
        (col("status") == "PLACED") &
        (col("payment_status") == "REFUNDED")
    )
)

invalid_orders = parsed_df.subtract(valid_orders)

def write_to_postgres(batch_df, batch_id):
    row_count = batch_df.count()
    print("Rows received:", row_count)
    print(f"Writing batch {batch_id} to PostgreSQL...")


    (
        batch_df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://postgres:5432/postgres")
        .option("dbtable", "orders")
        .option("user", "postgres")
        .option("password", "sanjana11")
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

query = (
    valid_orders.writeStream
    .foreachBatch(write_to_postgres)
    .outputMode("append")
    .option("checkpointLocation", "/tmp/checkpoints/orders")
    .start()
)

query.awaitTermination()