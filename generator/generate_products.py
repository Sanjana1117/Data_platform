import random
import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

OUTPUT = "data/generated/products.csv"

# --------------------------------------------------
# Load master data
# --------------------------------------------------

categories = pd.read_csv("data/generated/categories.csv")
brands = pd.read_csv("data/generated/brands.csv")

# --------------------------------------------------
# Product templates
# --------------------------------------------------

PRODUCT_TEMPLATES = {
    "Mobiles": [
        "Galaxy", "iPhone", "Pixel", "Nord",
        "Edge", "Note", "Pro", "Ultra"
    ],

    "Laptops": [
        "Inspiron", "Pavilion", "Yoga",
        "IdeaPad", "Vivobook", "Zenbook",
        "Predator", "Nitro"
    ],

    "Audio": [
        "Earbuds", "Headphones",
        "Speaker", "Soundbar"
    ],

    "Monitors": [
        "UltraGear",
        "Curved Monitor",
        "Gaming Monitor",
        "Business Monitor"
    ],

    "Storage": [
        "SSD",
        "Portable SSD",
        "Hard Drive",
        "USB Drive"
    ],

    "Smart Home": [
        "Smart Bulb",
        "Smart Plug",
        "Smart Camera",
        "Smart Hub"
    ],

    "Gaming": [
        "Gaming Mouse",
        "Gaming Keyboard",
        "Gaming Chair",
        "Gaming Controller"
    ],

    "Wearables": [
        "Smart Watch",
        "Fitness Band"
    ],

    "Printers": [
        "Inkjet Printer",
        "Laser Printer"
    ],

    "Networking": [
        "WiFi Router",
        "Mesh Router",
        "Network Switch"
    ]
}

products = []

product_id = 1

while len(products) < Config.NUM_PRODUCTS:

    brand = brands.sample(1).iloc[0]
    category = categories.sample(1).iloc[0]

    category_name = category["category_name"]

    if category_name not in PRODUCT_TEMPLATES:
        continue

    base_name = random.choice(PRODUCT_TEMPLATES[category_name])

    model = random.randint(100,999)

    variant = random.choice([
        "",
        "Pro",
        "Plus",
        "Max",
        "Ultra"
    ])

    product_name = f"{brand['brand_name']} {base_name} {model} {variant}".strip()

    cost = random.randint(500,80000)

    mrp = random.randint(
        int(cost*1.20),
        int(cost*1.60)
    )

    min_discount = random.randint(5,15)

    max_discount = random.randint(
        min_discount,
        40
    )

    weight = round(
        random.uniform(0.1,10),
        2
    )

    products.append({

        "product_id": product_id,

        "sku": f"SKU{product_id:06}",

        "product_name": product_name,

        "brand_id": brand["brand_id"],

        "category_id": category["category_id"],

        "cost_price": cost,

        "mrp": mrp,

        "min_discount": min_discount,

        "max_discount": max_discount,

        "weight_kg": weight,

        "launch_year": random.randint(2021,2026)

    })

    product_id += 1

df = pd.DataFrame(products)

df.to_csv(
    OUTPUT,
    index=False
)

print(df.head())

print(f"\nGenerated {len(df)} products.")