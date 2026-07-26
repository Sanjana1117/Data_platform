from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_category_analytics(df: DataFrame) -> DataFrame:
    """
    Build category-level analytics from enriched_live_orders.
    """

    # Grand total revenue (used for contribution %)
    total_revenue = (
        df.agg(
            F.sum("amount").alias("grand_total")
        )
        .first()["grand_total"]
    )

    category_df = (
        df.groupBy(
            "category_name",
            "department"
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
                F.avg("selling_price"),
                2
            ).alias("avg_selling_price"),

            F.countDistinct("customer_id").alias("unique_customers"),

            F.countDistinct("seller_product_id").alias("unique_products")

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

    return category_df