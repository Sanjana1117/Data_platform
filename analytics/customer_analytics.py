from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_customer_analytics(df: DataFrame) -> DataFrame:
    """
    Build customer-level analytics from enriched_live_orders.
    """

    # Grand total revenue (used for contribution %)
    total_revenue = (
        df.agg(
            F.sum("amount").alias("grand_total")
        )
        .first()["grand_total"]
    )

    customer_df = (
        df.groupBy(
            "customer_id",
            "first_name",
            "last_name",
            "customer_city",
            "customer_state",
            "membership"
        )
        .agg(

            F.count("order_id").alias("total_orders"),

            F.sum("quantity").alias("total_units"),

            F.round(
                F.sum("amount"),
                2
            ).alias("total_revenue"),

            F.round(
                F.avg("amount"),
                2
            ).alias("avg_order_value"),

            F.round(
                F.avg("quantity"),
                2
            ).alias("avg_items_per_order"),

            F.min(
                F.to_date("timestamp")
            ).alias("first_purchase_date"),

            F.max(
                F.to_date("timestamp")
            ).alias("last_purchase_date")
        )
        .withColumn(
            "active_days",
            F.datediff(
                F.col("last_purchase_date"),
                F.col("first_purchase_date")
            ) + 1
        )
        .withColumn(
            "revenue_contribution_pct",
            F.round(
                (F.col("total_revenue") / F.lit(total_revenue)) * 100,
                2
            )
        )
        .orderBy(
            F.desc("total_revenue")
        )
    )

    return customer_df