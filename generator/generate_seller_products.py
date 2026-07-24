import random
import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

OUTPUT = "data/generated/seller_products.csv"

# ---------------------------------------
# Load master tables
# ---------------------------------------

products = pd.read_csv("data/generated/products.csv")
sellers = pd.read_csv("data/generated/sellers.csv")

seller_products = []

used_pairs = set()

# ---------------------------------------
# Assign sellers to every product
# ---------------------------------------

for _, product in products.iterrows():

    seller_count = random.randint(
        Config.SELLERS_PER_PRODUCT[0],
        Config.SELLERS_PER_PRODUCT[1]
    )

    selected_sellers = sellers.sample(seller_count)

    for _, seller in selected_sellers.iterrows():

        pair = (
            seller["seller_id"],
            product["product_id"]
        )

        if pair in used_pairs:
            continue

        used_pairs.add(pair)

        cost = product["cost_price"]
        mrp = product["mrp"]

        selling_price = random.randint(
            cost + 1,
            mrp - 1
        )

        seller_products.append({

            "seller_id": seller["seller_id"],

            "product_id": product["product_id"],

            "selling_price": selling_price

        })

df = pd.DataFrame(seller_products)

df.sort_values(
    ["product_id", "seller_id"],
    inplace=True
)

df.to_csv(
    OUTPUT,
    index=False
)

print(df.head())

print(f"\nGenerated {len(df)} seller-product mappings.")

