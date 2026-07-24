from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
statuses = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED"]
payment_statuses = ["PAID", "PENDING", "REFUNDED"]

order_id = 1001


def generate_valid_order():
    global order_id

    order = {
        "order_id": order_id,
        "customer_id": random.randint(100, 999),
        "product": random.choice(products),
        "quantity": random.randint(1, 5),
        "amount": random.randint(500, 80000),
        "status": random.choice(statuses),
        "payment_status": random.choice(payment_statuses),
        "timestamp": datetime.now().isoformat()
    }

    order_id += 1
    return order


def generate_invalid_order():
    global order_id

    scenario = random.choice([
        "missing_order_id",
        "duplicate_order_id",
        "negative_amount",
        "zero_amount",
        "missing_customer",
        "invalid_customer",
        "missing_product",
        "empty_product",
        "unknown_product",
        "missing_quantity",
        "zero_quantity",
        "future_timestamp",
        "cancelled_but_paid",
        "placed_but_refunded",
        "huge_amount"
    ])

    order = {
        "order_id": order_id,
        "customer_id": random.randint(100, 999),
        "product": random.choice(products),
        "quantity": random.randint(1, 5),
        "amount": random.randint(500, 80000),
        "status": "PLACED",
        "payment_status": "PAID",
        "timestamp": datetime.now().isoformat()
    }

    if scenario == "missing_order_id":
        order["order_id"] = None

    elif scenario == "duplicate_order_id":
        # Don't increment order_id so the next event uses the same ID
        pass

    elif scenario == "negative_amount":
        order["amount"] = -5000

    elif scenario == "zero_amount":
        order["amount"] = 0

    elif scenario == "missing_customer":
        order["customer_id"] = None

    elif scenario == "invalid_customer":
        order["customer_id"] = -1

    elif scenario == "missing_product":
        order["product"] = None

    elif scenario == "empty_product":
        order["product"] = ""

    elif scenario == "unknown_product":
        order["product"] = "iPhone"

    elif scenario == "missing_quantity":
        order["quantity"] = None

    elif scenario == "zero_quantity":
        order["quantity"] = 0

    elif scenario == "future_timestamp":
        order["timestamp"] = "2035-01-01T10:00:00"

    elif scenario == "cancelled_but_paid":
        order["status"] = "CANCELLED"
        order["payment_status"] = "PAID"

    elif scenario == "placed_but_refunded":
        order["status"] = "PLACED"
        order["payment_status"] = "REFUNDED"

    elif scenario == "huge_amount":
        order["amount"] = 999999999

    if scenario != "duplicate_order_id":
        order_id += 1

    return order


while True:

    # Approximately 20% invalid events
    if random.randint(1, 5) == 1:
        order = generate_invalid_order()
        print("❌ INVALID EVENT")
    else:
        order = generate_valid_order()
        print("✅ VALID EVENT")

    print(order)

    producer.send("orders", order)
    producer.flush()

    time.sleep(2)