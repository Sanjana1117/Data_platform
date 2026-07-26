from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime
from pathlib import Path
import sys

import pandas as pd

# =====================================================
# Project Imports
# =====================================================

sys.path.append(str(Path(__file__).resolve().parent.parent))

from generator.config import Config

# =====================================================
# Kafka Producer
# =====================================================

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =====================================================
# Load Master Data
# =====================================================

customers_df = pd.read_csv(Config.CUSTOMERS_FILE)

seller_products_df = pd.read_csv(Config.SELLER_PRODUCTS_FILE)

warehouse_inventory_df = pd.read_csv(
    Config.WAREHOUSE_INVENTORY_FILE
)

# =====================================================
# Lookup Lists
# =====================================================

customer_ids = customers_df["customer_id"].tolist()

statuses = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED"
]

order_id = 10001

# =====================================================
# Generate Valid Event
# =====================================================

def generate_valid_event():

    global order_id

    customer_id = random.choice(customer_ids)

    seller_product = seller_products_df.sample(1).iloc[0]

    seller_product_id = int(
        seller_product["seller_product_id"]
    )

    selling_price = float(
        seller_product["selling_price"]
    )

    inventory_rows = warehouse_inventory_df[
        warehouse_inventory_df["seller_product_id"]
        == seller_product_id
    ]

    inventory = inventory_rows.sample(1).iloc[0]

    warehouse_inventory_id = int(
        inventory["warehouse_inventory_id"]
    )

    quantity = random.randint(1, 5)

    amount = quantity * selling_price

    status = random.choice(statuses)

    if status == "PLACED":
        payment_status = random.choice(
            ["PAID", "PENDING"]
        )

    elif status == "SHIPPED":
        payment_status = "PAID"

    elif status == "DELIVERED":
        payment_status = "PAID"

    else:
        payment_status = random.choice(
            ["PENDING", "REFUNDED"]
        )

    event = {
        "order_id": order_id,
        "customer_id": customer_id,
        "seller_product_id": seller_product_id,
        "warehouse_inventory_id": warehouse_inventory_id,
        "quantity": quantity,
        "selling_price": selling_price,
        "amount": amount,
        "status": status,
        "payment_status": payment_status,
        "timestamp": datetime.now().isoformat()
    }

    order_id += 1

    return event


# =====================================================
# Generate Invalid Event
# =====================================================

def generate_invalid_event():

    event = generate_valid_event()

    scenario = random.choice([
        "missing_order_id",
        "duplicate_order_id",
        "invalid_customer",
        "invalid_seller_product",
        "invalid_inventory",
        "negative_quantity",
        "negative_price",
        "negative_amount",
        "future_timestamp",
        "cancelled_paid",
        "placed_refunded"
    ])

    if scenario == "missing_order_id":
        event["order_id"] = None

    elif scenario == "duplicate_order_id":
        event["order_id"] -= 1

    elif scenario == "invalid_customer":
        event["customer_id"] = -1

    elif scenario == "invalid_seller_product":
        event["seller_product_id"] = -1

    elif scenario == "invalid_inventory":
        event["warehouse_inventory_id"] = -1

    elif scenario == "negative_quantity":
        event["quantity"] = -2

    elif scenario == "negative_price":
        event["selling_price"] = -100

    elif scenario == "negative_amount":
        event["amount"] = -500

    elif scenario == "future_timestamp":
        event["timestamp"] = "2035-01-01T10:00:00"

    elif scenario == "cancelled_paid":
        event["status"] = "CANCELLED"
        event["payment_status"] = "PAID"

    elif scenario == "placed_refunded":
        event["status"] = "PLACED"
        event["payment_status"] = "REFUNDED"

    return event


# =====================================================
# Produce Events
# =====================================================

print("===================================")
print("NovaCart Producer Started")
print(f"Customers Loaded        : {len(customers_df)}")
print(f"Seller Products Loaded  : {len(seller_products_df)}")
print(f"Inventory Rows Loaded   : {len(warehouse_inventory_df)}")
print("===================================\n")

while True:

    if random.random() < 0.8:

        event = generate_valid_event()
        print("✅ VALID EVENT")

    else:

        event = generate_invalid_event()
        print("❌ INVALID EVENT")

    print(json.dumps(event, indent=2))

    producer.send("order_events", event)
    producer.flush()

    print("-" * 60)

    time.sleep(2)