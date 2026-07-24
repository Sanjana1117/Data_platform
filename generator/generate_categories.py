import pandas as pd
from config import Config

OUTPUT = Config.CATEGORIES_FILE

categories = [
    ("Electronics", "Electronics", 18),
    ("Mobiles", "Electronics", 18),
    ("Laptops", "Electronics", 18),
    ("Computer Accessories", "Electronics", 18),
    ("Gaming", "Electronics", 18),
    ("Audio", "Electronics", 18),
    ("Cameras", "Electronics", 18),
    ("Wearables", "Electronics", 18),
    ("Printers", "Electronics", 18),
    ("Networking", "Electronics", 18),
    ("Storage", "Electronics", 18),
    ("Monitors", "Electronics", 18),
    ("Smart Home", "Electronics", 18),
    ("Furniture", "Home", 18),
    ("Kitchen", "Home", 18),
    ("Home Appliances", "Home", 18),
    ("Home Decor", "Home", 12),
    ("Lighting", "Home", 12),
    ("Garden", "Home", 12),
    ("Tools", "Home", 18),
    ("Automotive", "Auto", 28),
    ("Motorcycle", "Auto", 28),
    ("Books", "Books", 0),
    ("Stationery", "Office", 12),
    ("Office Supplies", "Office", 18),
    ("Sports", "Sports", 12),
    ("Fitness", "Sports", 18),
    ("Health", "Health", 12),
    ("Beauty", "Beauty", 18),
    ("Personal Care", "Beauty", 18),
    ("Fashion Men", "Fashion", 12),
    ("Fashion Women", "Fashion", 12),
    ("Fashion Kids", "Fashion", 12),
    ("Footwear", "Fashion", 12),
    ("Jewellery", "Fashion", 3),
    ("Watches", "Fashion", 18),
    ("Luggage", "Travel", 18),
    ("Travel", "Travel", 18),
    ("Party Supplies", "Lifestyle", 18),
    ("Groceries", "Grocery", 5),
    ("Beverages", "Grocery", 12),
    ("Snacks", "Grocery", 12),
    ("Frozen Foods", "Grocery", 5),
    ("Cleaning", "Home", 18),
    ("Pet Supplies", "Lifestyle", 12),
    ("Baby Care", "Lifestyle", 12),
    ("Toys", "Lifestyle", 12),
    ("Art & Crafts", "Lifestyle", 12),
    ("Medical Supplies", "Health", 5),
    ("Seasonal", "Lifestyle", 18),
]

df = pd.DataFrame(
    categories,
    columns=["category_name", "department", "gst_percentage"],
)

df.insert(0, "category_id", range(1, len(df) + 1))

df.to_csv(OUTPUT, index=False)

print("✅ categories.csv generated")