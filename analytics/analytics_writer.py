from pyspark.sql import DataFrame


def write_analytics_table(
    df: DataFrame,
    table_name: str,
    jdbc_url: str,
    db_properties: dict
) -> None:

    (
        df.write
        .mode("overwrite")
        .jdbc(
            url=jdbc_url,
            table=table_name,
            properties=db_properties
        )
    )

    print(f"✓ {table_name} updated successfully")