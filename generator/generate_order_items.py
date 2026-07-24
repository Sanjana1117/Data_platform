import random
import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

# -------------------------
# Configuration
# -------------------------

OUTPUT = Config.ORDER_ITEMS_FILE

MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

# -------------------------
# Read Data
# -------------------------

orders = pd.read_csv(Config.ORDERS_FILE)

products = pd.read_csv(Config.PRODUCTS_FILE)

seller_products = pd.read_csv(
    Config.SELLER_PRODUCTS_FILE
)

inventory = pd.read_csv(
    Config.WAREHOUSE_INVENTORY_FILE
)

categories = pd.read_csv(
    Config.CATEGORIES_FILE
)

# -------------------------
# Lookup Dictionaries
# -------------------------

# product_id -> product row
product_lookup = (
    products
    .set_index("product_id")
    .to_dict("index")
)

# category_id -> category row
category_lookup = (
    categories
    .set_index("category_id")
    .to_dict("index")
)

# product_id -> all seller listings for that product
seller_products_by_product = (
    seller_products
    .groupby("product_id")
)

# seller_product_id -> seller product row
seller_product_lookup = (
    seller_products
    .set_index("seller_product_id")
    .to_dict("index")
)

# seller_product_id -> inventory rows
inventory_lookup = (
    inventory
    .groupby("seller_product_id")
)

# warehouse_inventory_id -> inventory row
warehouse_inventory_lookup = (
    inventory
    .set_index("warehouse_inventory_id")
    .to_dict("index")
)

# category_id -> gst percentage
gst_lookup = (
    categories
    .set_index("category_id")["gst_percentage"]
    .to_dict()
)

# -------------------------
# Output Container
# -------------------------

order_items = []

order_item_id = 1