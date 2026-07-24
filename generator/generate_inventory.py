import random
from datetime import datetime

import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

OUTPUT = Config.WAREHOUSE_INVENTORY_FILE

seller_products = pd.read_csv(Config.SELLER_PRODUCTS_FILE)
warehouses = pd.read_csv(Config.WAREHOUSES_FILE)

inventory = []

used = set()

warehouse_inventory_id = 1

for _, row in seller_products.iterrows():

    warehouse_count = random.randint(
        Config.WAREHOUSES_PER_SELLER_PRODUCT[0],
        Config.WAREHOUSES_PER_SELLER_PRODUCT[1]
    )

    remaining_stock = random.randint(
        Config.MIN_STOCK,
        Config.MAX_STOCK
    )

    warehouse_count = min(
        warehouse_count,
        remaining_stock
    )

    selected = warehouses.sample(warehouse_count)

    for i, (_, warehouse) in enumerate(selected.iterrows()):

        if i == warehouse_count - 1:

            stock = remaining_stock

        else:

            warehouses_left = warehouse_count - i - 1

            max_stock = remaining_stock - warehouses_left

            stock = random.randint(
                1,
                max_stock
            )

            remaining_stock -= stock

        key = (
            warehouse["warehouse_id"],
            row["seller_product_id"]
        )

        if key in used:
            continue

        used.add(key)

        inventory.append({

            "warehouse_inventory_id": warehouse_inventory_id,

            "warehouse_id": warehouse["warehouse_id"],

            "seller_product_id": row["seller_product_id"],

            "stock_quantity": stock,

            "last_updated": datetime.now().strftime("%Y-%m-%d")

        })

        warehouse_inventory_id += 1

df = pd.DataFrame(inventory)

df.sort_values(
    ["warehouse_id", "seller_product_id"],
    inplace=True
)

df.to_csv(
    OUTPUT,
    index=False
)

print(df.head())

print(f"\nGenerated {len(df)} warehouse inventory records.")