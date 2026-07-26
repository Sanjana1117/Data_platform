from pyspark.sql.functions import col, lit, when


def validate_orders(df):

    validated_df = (
        df.withColumn(
            "reason",
            when(col("order_id").isNull(), "INVALID_ORDER_ID")

            .when(
                col("customer_id").isNull() |
                (col("customer_id") <= 0),
                "INVALID_CUSTOMER_ID"
            )

            .when(
                col("seller_product_id").isNull() |
                (col("seller_product_id") <= 0),
                "INVALID_SELLER_PRODUCT_ID"
            )

            .when(
                col("warehouse_inventory_id").isNull() |
                (col("warehouse_inventory_id") <= 0),
                "INVALID_WAREHOUSE_ID"
            )

            .when(
                col("quantity").isNull() |
                (col("quantity") <= 0),
                "INVALID_QUANTITY"
            )

            .when(
                col("selling_price").isNull() |
                (col("selling_price") <= 0),
                "INVALID_SELLING_PRICE"
            )

            .when(
                col("amount").isNull() |
                (col("amount") <= 0),
                "INVALID_AMOUNT"
            )

            .when(
                col("timestamp").isNull(),
                "INVALID_TIMESTAMP"
            )

            .when(
                ~col("status").isin(
                    "PLACED",
                    "SHIPPED",
                    "DELIVERED",
                    "CANCELLED"
                ),
                "INVALID_STATUS"
            )

            .when(
                ~col("payment_status").isin(
                    "PAID",
                    "PENDING",
                    "REFUNDED"
                ),
                "INVALID_PAYMENT_STATUS"
            )

            .when(
                (col("status") == "CANCELLED") &
                (col("payment_status") == "PAID"),
                "INVALID_STATUS_PAYMENT_COMBINATION"
            )

            .when(
                (col("status") == "PLACED") &
                (col("payment_status") == "REFUNDED"),
                "INVALID_STATUS_PAYMENT_COMBINATION"
            )

            .otherwise(lit(None))
        )
    )

    valid_orders = validated_df.filter(col("reason").isNull())

    invalid_orders = validated_df.filter(col("reason").isNotNull())

    return valid_orders, invalid_orders