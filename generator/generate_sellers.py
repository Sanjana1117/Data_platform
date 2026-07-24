import random
import pandas as pd

from faker import Faker
from config import Config

fake = Faker("en_IN")
random.seed(Config.RANDOM_SEED)
Faker.seed(Config.RANDOM_SEED)

OUTPUT = "data/generated/sellers.csv"

# --------------------------------------------------
# Company Name Components
# --------------------------------------------------

PREFIXES = [
    "Tech", "Digital", "Smart", "Elite", "Prime",
    "Modern", "Future", "Global", "Metro", "National",
    "Urban", "Mega", "Nova", "Infinity", "Royal"
]

BUSINESSES = [
    "Electronics", "Retail", "Traders", "Solutions",
    "Computers", "Mobiles", "Marketplace", "Stores",
    "Enterprises", "Distributors", "Hub", "World",
    "Mart", "Systems", "Technologies"
]

sellers = []

for seller_id in range(1, Config.NUM_SELLERS + 1):

    company = f"{random.choice(PREFIXES)} {random.choice(BUSINESSES)}"

    sellers.append({
        "seller_id": seller_id,
        "seller_name": company,
        "city": fake.city(),
        "state": fake.state(),
        "country": "India",
        "seller_rating": round(random.uniform(3.5, 5.0), 1),
        "verified": random.random() < 0.8,
        "seller_since": fake.date_between(
            start_date="-8y",
            end_date="today"
        )
    })

df = pd.DataFrame(sellers)

df.to_csv(
    OUTPUT,
    index=False
)

print(df.head())

print(f"\nGenerated {len(df)} sellers.")