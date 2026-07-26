from pyspark.sql.functions import col


def load_master_data(spark):

    from generator.config import Config

    products = (
        spark.read.option("header", True)
        .csv(str(Config.PRODUCTS_FILE))
    )

    seller_products = (
        spark.read.option("header", True)
        .csv(str(Config.SELLER_PRODUCTS_FILE))
    )

    sellers = (
        spark.read.option("header", True)
        .csv(str(Config.SELLERS_FILE))
    )

    brands = (
        spark.read.option("header", True)
        .csv(str(Config.BRANDS_FILE))
    )

    categories = (
        spark.read.option("header", True)
        .csv(str(Config.CATEGORIES_FILE))
    )

    inventory = (
        spark.read.option("header", True)
        .csv(str(Config.WAREHOUSE_INVENTORY_FILE))
    )

    warehouses = (
        spark.read.option("header", True)
        .csv(str(Config.WAREHOUSES_FILE))
    )

    customers = (
        spark.read.option("header", True)
        .csv(str(Config.CUSTOMERS_FILE))
    )

    return {
        "products": products,
        "seller_products": seller_products,
        "sellers": sellers,
        "brands": brands,
        "categories": categories,
        "inventory": inventory,
        "warehouses": warehouses,
        "customers": customers,
    }


def enrich_orders(valid_df, master_data):

    customers = master_data["customers"]
    seller_products = master_data["seller_products"]
    sellers = master_data["sellers"]
    products = master_data["products"]
    brands = master_data["brands"]
    categories = master_data["categories"]
    inventory = master_data["inventory"]
    warehouses = master_data["warehouses"]

    enriched = (
        valid_df.alias("o")

        .join(
            customers.alias("c"),
            col("o.customer_id") == col("c.customer_id"),
            "left"
        )

        .join(
            seller_products.alias("sp"),
            col("o.seller_product_id") == col("sp.seller_product_id"),
            "left"
        )

        .join(
            sellers.alias("s"),
            col("sp.seller_id") == col("s.seller_id"),
            "left"
        )

        .join(
            products.alias("p"),
            col("sp.product_id") == col("p.product_id"),
            "left"
        )

        .join(
            brands.alias("b"),
            col("p.brand_id") == col("b.brand_id"),
            "left"
        )

        .join(
            categories.alias("cat"),
            col("p.category_id") == col("cat.category_id"),
            "left"
        )

        .join(
            inventory.alias("i"),
            col("o.warehouse_inventory_id") == col("i.warehouse_inventory_id"),
            "left"
        )

        .join(
            warehouses.alias("w"),
            col("i.warehouse_id") == col("w.warehouse_id"),
            "left"
        )

        .select(

            # Stream columns
            col("o.order_id"),
            col("o.customer_id"),
            col("o.seller_product_id"),
            col("o.warehouse_inventory_id"),
            col("o.quantity"),
            col("o.selling_price"),
            col("o.amount"),
            col("o.status"),
            col("o.payment_status"),
            col("o.timestamp"),

            # Customer
            col("c.first_name"),
            col("c.last_name"),
            col("c.city").alias("customer_city"),
            col("c.state").alias("customer_state"),
            col("c.membership"),

            # Seller
            col("s.seller_name"),
            col("s.seller_rating"),

            # Product
            col("p.product_name"),
            col("p.sku"),
            col("p.weight_kg"),

            # Brand
            col("b.brand_name"),

            # Category
            col("cat.category_name"),
            col("cat.department"),

            # Warehouse
            col("w.warehouse_name"),
            col("w.city").alias("warehouse_city"),
            col("w.state").alias("warehouse_state"),
        )
    )

    return enriched