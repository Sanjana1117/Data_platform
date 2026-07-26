from pyspark.sql.functions import col, current_timestamp

def validate_orders(df):

    return df.filter(

        col("order_id").isNotNull() &
        col("customer_id").isNotNull() &
        (col("customer_id") > 0) &

        col("seller_product_id").isNotNull() &
        (col("seller_product_id") > 0) &

        col("warehouse_inventory_id").isNotNull() &
        (col("warehouse_inventory_id") > 0) &

        col("quantity").isNotNull() &
        (col("quantity") > 0) &

        col("selling_price").isNotNull() &
        (col("selling_price") > 0) &

        col("amount").isNotNull() &
        (col("amount") > 0) &

        col("timestamp").isNotNull() &
        #(col("timestamp") <= current_timestamp()) &

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