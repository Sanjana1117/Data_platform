from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp, to_timestamp
from pyspark.sql.types import *
from spark.schemas import ORDER_EVENT_SCHEMA
from spark.validation import validate_orders
from spark.postgres_writer import write_to_postgres
from spark.enrichment import load_master_data, enrich_orders
from analytics.sales_analytics import build_sales_analytics
from analytics.category_analytics import build_category_analytics
from analytics.product_analytics import build_product_analytics
from analytics.seller_analytics import build_seller_analytics
from analytics.customer_analytics import build_customer_analytics
from analytics.warehouse_analytics import build_warehouse_analytics
from analytics.brand_analytics import build_brand_analytics
from analytics.data_quality_analytics import build_data_quality_analytics
from analytics.analytics_writer import write_analytics_tables

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

jdbc_url = "jdbc:postgresql://postgres:5432/enterprise_db"

connection_properties = {
    "user": "postgres",
    "password": "sanjana11",
    "driver": "org.postgresql.Driver"
}

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

#valid_orders, invalid_orders = validate_orders(parsed_df)

# ==========================================
# Start Streaming
# ==========================================



def process_batch(batch_df, batch_id):

    # Validate records
    valid_df, invalid_df = validate_orders(batch_df)

    # Enrich valid records
    enriched_df = enrich_orders(valid_df, master_data)

    enriched_df.printSchema()

    # Write operational tables
    write_to_postgres(
        batch_df,
        enriched_df,
        invalid_df,
        batch_id
    )

    # ==========================
    # Build Analytics
    # ==========================

    sales_df = build_sales_analytics(enriched_df)

    category_df = build_category_analytics(enriched_df)

    product_df = build_product_analytics(enriched_df)

    seller_df = build_seller_analytics(enriched_df)

    customer_df = build_customer_analytics(enriched_df)

    warehouse_df = build_warehouse_analytics(enriched_df)

    brand_df = build_brand_analytics(enriched_df)

    data_quality_df = build_data_quality_analytics(
        valid_df,
        invalid_df
    )

    # ==========================
    # Write Analytics Tables
    # ==========================

    write_analytics_tables(
        sales_df,
        category_df,
        product_df,
        seller_df,
        customer_df,
        warehouse_df,
        brand_df,
        data_quality_df,
        jdbc_url,
        connection_properties
    )


query = (
    parsed_df.writeStream
    .foreachBatch(process_batch)
    .outputMode("append")
    .option("checkpointLocation", "/tmp/checkpoints/order_events")
    .start()
)

query.awaitTermination()

# query = (
#     valid_orders.writeStream
#     .foreachBatch(write_to_postgres)
#     .outputMode("append")
#     .option("checkpointLocation", "/tmp/checkpoints/order_events")
#     .start()
# )

# query.awaitTermination()






