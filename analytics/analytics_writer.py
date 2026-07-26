from pyspark.sql import DataFrame


def write_analytics_tables(
    sales_df: DataFrame,
    category_df: DataFrame,
    product_df: DataFrame,
    seller_df: DataFrame,
    customer_df: DataFrame,
    warehouse_df: DataFrame,
    brand_df: DataFrame,
    data_quality_df: DataFrame,
    jdbc_url: str,
    connection_properties: dict,
):
    """
    Write all analytics DataFrames to PostgreSQL.
    """

    analytics_tables = {
        "analytics_sales": sales_df,
        "analytics_category": category_df,
        "analytics_product": product_df,
        "analytics_seller": seller_df,
        "analytics_customer": customer_df,
        "analytics_warehouse": warehouse_df,
        "analytics_brand": brand_df,
        "analytics_data_quality": data_quality_df,
    }

    for table_name, dataframe in analytics_tables.items():
        (
            dataframe.write
            .mode("overwrite")
            .jdbc(
                url=jdbc_url,
                table=table_name,
                properties=connection_properties,
            )
        )

    print("All analytics tables updated successfully.")