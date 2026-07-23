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
    StructField("amount", IntegerType(), True),
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

def write_to_postgres(batch_df, batch_id):
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
    parsed_df.writeStream
    .foreachBatch(write_to_postgres)
    .outputMode("append")
    .option("checkpointLocation", "/tmp/checkpoints/orders")
    .start()
)

query.awaitTermination()