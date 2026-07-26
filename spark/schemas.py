# ==========================================
# Schema of Kafka Event
# ==========================================

from pyspark.sql.types import *

ORDER_EVENT_SCHEMA = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("seller_product_id", IntegerType(), True),
    StructField("warehouse_inventory_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("selling_price", DoubleType(), True),
    StructField("amount", DoubleType(), True),
    StructField("status", StringType(), True),
    StructField("payment_status", StringType(), True),
    StructField("timestamp", StringType(), True)
])