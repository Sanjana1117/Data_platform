from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    avg,
    col,
    count,
    countDistinct,
    round,
    sum,
    to_date,
    when
)


def build_sales_analytics(enriched_df: DataFrame) -> DataFrame:

    sales_df = (
        enriched_df
        .withColumn("sales_date", to_date(col("timestamp")))
        .groupBy("sales_date")
        .agg(

            count("order_id").alias("total_orders"),

            round(sum("amount"), 2).alias("total_revenue"),

            sum("quantity").alias("total_units"),

            round(avg("amount"), 2).alias("avg_order_value"),

            round(avg("quantity"), 2).alias("avg_items_per_order"),

            countDistinct("customer_id").alias("unique_customers"),

            countDistinct("product_name").alias("unique_products"),

            sum(
                when(col("status") == "CANCELLED", 1).otherwise(0)
            ).alias("cancelled_orders"),

            sum(
                when(col("payment_status") == "PAID", 1).otherwise(0)
            ).alias("successful_payments")
        )
        .withColumn(
            "cancellation_rate",
            round(
                (col("cancelled_orders") / col("total_orders")) * 100,
                2
            )
        )
        .withColumn(
            "payment_success_rate",
            round(
                (col("successful_payments") / col("total_orders")) * 100,
                2
            )
        )
    )

    return sales_df