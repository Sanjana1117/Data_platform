from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp, to_timestamp
from pyspark.sql.types import *
from spark.schemas import ORDER_EVENT_SCHEMA
from spark.validation import validate_orders
from spark.postgres_writer import write_to_postgres
from spark.enrichment import load_master_data


spark = (
    SparkSession.builder
    .appName("NovaCart")
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0",
            "org.postgresql:postgresql:42.7.7"
        ])
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

master_data = load_master_data(spark)

# ==========================================
# Read Kafka Stream
# ==========================================

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "order_events")
    .option("startingOffsets", "earliest")
    .load()
)

# ==========================================
# Parse JSON
# ==========================================

parsed_df = (
    df.selectExpr("CAST(value AS STRING) as value")
      .select(from_json(col("value"), ORDER_EVENT_SCHEMA).alias("data"))
      .select("data.*")
      .withColumn("timestamp", to_timestamp(col("timestamp")))
)

valid_orders = validate_orders(parsed_df)

# ==========================================
# Start Streaming
# ==========================================

# query = (
#     valid_orders.writeStream
#     .foreachBatch(write_to_postgres)
#     .outputMode("append")
#     #.option("checkpointLocation", "/tmp/checkpoints/order_events")
#     .start()
# )

# query.awaitTermination()


# query = (
#     df.selectExpr(
#         "CAST(value AS STRING) as value",
#         "topic",
#         "partition",
#         "offset"
#     )
#     .writeStream
#     .format("console")
#     .outputMode("append")
#     .option("truncate", "false")
#     .start()
# )

# query.awaitTermination()

query = (
    parsed_df.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .start()
)

query.awaitTermination()


