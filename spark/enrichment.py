from pyspark.sql.types import *

from generator.config import Config


def load_master_data(spark):

    products = (
        spark.read
        .option("header", True)
        .csv(str(Config.PRODUCTS_FILE))
    )

    seller_products = (
        spark.read
        .option("header", True)
        .csv(str(Config.SELLER_PRODUCTS_FILE))
    )

    brands = (
        spark.read
        .option("header", True)
        .csv(str(Config.BRANDS_FILE))
    )

    categories = (
        spark.read
        .option("header", True)
        .csv(str(Config.CATEGORIES_FILE))
    )

    inventory = (
        spark.read
        .option("header", True)
        .csv(str(Config.WAREHOUSE_INVENTORY_FILE))
    )

    warehouses = (
        spark.read
        .option("header", True)
        .csv(str(Config.WAREHOUSES_FILE))
    )

    customers = (
        spark.read
        .option("header", True)
        .csv(str(Config.CUSTOMERS_FILE))
    )

    return {
        "products": products,
        "seller_products": seller_products,
        "brands": brands,
        "categories": categories,
        "inventory": inventory,
        "warehouses": warehouses,
        "customers": customers
    }