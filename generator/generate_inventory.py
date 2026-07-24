import random
import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

OUTPUT = "data/generated/warehouse_inventory.csv"

seller_products = pd.read_csv(
    "data/generated/seller_products.csv"
)

warehouses = pd.read_csv(
    "data/generated/warehouses.csv"
)

inventory = []

used = set()

for _, row in seller_products.iterrows():

    warehouse_count = random.randint(
        Config.WAREHOUSES_PER_SELLER_PRODUCT[0],
        Config.WAREHOUSES_PER_SELLER_PRODUCT[1]
    )

    selected = warehouses.sample(warehouse_count)

    remaining_stock = random.randint(
        Config.MIN_STOCK,
        Config.MAX_STOCK
    )

    for i, (_, warehouse) in enumerate(selected.iterrows()):

        if i == warehouse_count - 1:

            stock = remaining_stock

        else:

            stock = random.randint(
                1,
                remaining_stock
            )

            remaining_stock -= stock

        key = (

            warehouse["warehouse_id"],

            row["seller_id"],

            row["product_id"]

        )

        if key in used:
            continue

        used.add(key)

        inventory.append({

            "warehouse_id": warehouse["warehouse_id"],

            "seller_id": row["seller_id"],

            "product_id": row["product_id"],

            "stock_quantity": stock,

            "last_updated": "2026-07-24"

        })

df = pd.DataFrame(inventory)

df.to_csv(
    OUTPUT,
    index=False
)

print(df.head())

print(f"\nGenerated {len(df)} inventory records.")

