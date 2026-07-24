import random
import pandas as pd

from config import Config

random.seed(Config.RANDOM_SEED)

OUTPUT = Config.WAREHOUSES_FILE

WAREHOUSE_LOCATIONS = [
    ("Chennai", "Tamil Nadu"),
    ("Bangalore", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Noida", "Uttar Pradesh"),
    ("Gurugram", "Haryana"),
    ("Ahmedabad", "Gujarat"),
    ("Surat", "Gujarat"),
    ("Jaipur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
    ("Kolkata", "West Bengal"),
    ("Bhubaneswar", "Odisha"),
    ("Patna", "Bihar"),
    ("Indore", "Madhya Pradesh"),
    ("Nagpur", "Maharashtra"),
    ("Visakhapatnam", "Andhra Pradesh"),
    ("Kochi", "Kerala"),
    ("Coimbatore", "Tamil Nadu"),
    ("Madurai", "Tamil Nadu"),
    ("Mysore", "Karnataka"),
    ("Vijayawada", "Andhra Pradesh"),
    ("Raipur", "Chhattisgarh"),
    ("Bhopal", "Madhya Pradesh"),
    ("Chandigarh", "Chandigarh"),
    ("Goa", "Goa"),
    ("Ranchi", "Jharkhand"),
    ("Siliguri", "West Bengal"),
    ("Guwahati", "Assam")
]

warehouses = []

for warehouse_id, (city, state) in enumerate(WAREHOUSE_LOCATIONS, start=1):

    warehouses.append({

        "warehouse_id": warehouse_id,

        "warehouse_name": f"{city} Fulfillment Center",

        "city": city,

        "state": state,

        "country": Config.COUNTRY,

        "capacity": random.randint(100000, 500000)

    })

df = pd.DataFrame(warehouses)

df.to_csv(OUTPUT, index=False)

print(df.head())

print(f"\nGenerated {len(df)} warehouses.")