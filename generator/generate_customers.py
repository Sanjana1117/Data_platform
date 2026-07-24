import random
import pandas as pd

from faker import Faker
from config import Config

fake = Faker("en_IN")

random.seed(Config.RANDOM_SEED)
Faker.seed(Config.RANDOM_SEED)

OUTPUT = Config.CUSTOMERS_FILE

# -------------------------------------------------
# Indian Locations
# -------------------------------------------------

LOCATIONS = [
    ("Chennai","Tamil Nadu"),
    ("Coimbatore","Tamil Nadu"),
    ("Madurai","Tamil Nadu"),
    ("Bangalore","Karnataka"),
    ("Mysore","Karnataka"),
    ("Hyderabad","Telangana"),
    ("Warangal","Telangana"),
    ("Mumbai","Maharashtra"),
    ("Pune","Maharashtra"),
    ("Nagpur","Maharashtra"),
    ("Delhi","Delhi"),
    ("Noida","Uttar Pradesh"),
    ("Lucknow","Uttar Pradesh"),
    ("Ahmedabad","Gujarat"),
    ("Surat","Gujarat"),
    ("Jaipur","Rajasthan"),
    ("Kolkata","West Bengal"),
    ("Patna","Bihar"),
    ("Bhubaneswar","Odisha"),
    ("Kochi","Kerala")
]

MEMBERSHIPS = ["Regular", "Prime", "Premium"]
WEIGHTS = [0.70, 0.25, 0.05]

customers = []

for customer_id in range(1, Config.NUM_CUSTOMERS + 1):

    city, state = random.choice(LOCATIONS)

    customers.append({

        "customer_id": customer_id,

        "first_name": fake.first_name(),

        "last_name": fake.last_name(),

        "gender": random.choice(["Male","Female"]),

        "age": random.randint(18,70),

        "city": city,

        "state": state,

        "country": Config.COUNTRY,

        "pincode": fake.postcode(),

        "member_since": fake.date_between(
            start_date="-8y",
            end_date="today"
        ),

        "membership": random.choices(
            MEMBERSHIPS,
            weights=WEIGHTS,
            k=1
        )[0]

    })

df = pd.DataFrame(customers)

df.to_csv(
    OUTPUT,
    index=False
)

print(df.head())

print(f"\nGenerated {len(df)} customers.")