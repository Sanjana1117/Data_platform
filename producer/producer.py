from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]

order_id = 1001

while True:
    order = {
        "order_id": order_id,
        "customer_id": random.randint(100, 999),
        "product": random.choice(products),
        "amount": random.randint(500, 80000),
    }

    producer.send("orders", order)
    producer.flush()

    print(order)

    order_id += 1
    time.sleep(2)