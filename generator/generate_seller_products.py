import random
import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

OUTPUT = Config.SELLER_PRODUCTS_FILE

products = pd.read_csv(Config.PRODUCTS_FILE)
sellers = pd.read_csv(Config.SELLERS_FILE)

seller_products = []
seller_product_id = 1

used_pairs = set()

# ---------------------------------------
# Assign sellers to every product
# ---------------------------------------
min_sellers, max_sellers = Config.SELLERS_PER_PRODUCT

for _, product in products.iterrows():

    seller_count = random.randint(
        min_sellers,
        max_sellers
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

        discount = random.randint(
            product["min_discount"],
            product["max_discount"]
        )

        selling_price = int(
            mrp * (1 - discount / 100)
        )

        # Safety check
        selling_price = max(selling_price, cost + 1)

        seller_products.append({

            "seller_product_id": seller_product_id,

            "seller_id": seller["seller_id"],

            "product_id": product["product_id"],

            "selling_price": selling_price

        })

        seller_product_id += 1

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

