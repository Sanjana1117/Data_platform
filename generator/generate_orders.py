import random
from datetime import datetime, timedelta

import pandas as pd

# ==========================
# Configuration
# ==========================

NUM_ORDERS = 50000

ORDER_STATUSES = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED"
]

STATUS_WEIGHTS = [
    15,  # PLACED
    20,  # SHIPPED
    60,  # DELIVERED
    5    # CANCELLED
]

# ==========================
# Read Master Data
# ==========================

customers = pd.read_csv("data/generated/customers.csv")

# ==========================
# Helper Functions
# ==========================

def get_payment_status(order_status):
    if order_status in ["DELIVERED", "SHIPPED"]:
        return "PAID"

    if order_status == "PLACED":
        return random.choice([
            "PAID",
            "PENDING"
        ])

    return random.choice([
        "PENDING",
        "REFUNDED"
    ])


def random_order_date():
    start_date = datetime(2025, 1, 1)
    end_date = datetime.now()

    random_seconds = random.randint(
        0,
        int((end_date - start_date).total_seconds())
    )

    return (
        start_date + timedelta(seconds=random_seconds)
    ).strftime("%Y-%m-%d %H:%M:%S")


# ==========================
# Generate Orders
# ==========================

orders = []

customer_ids = customers["customer_id"].tolist()

for order_id in range(1, NUM_ORDERS + 1):

    customer_id = random.choice(customer_ids)

    order_status = random.choices(
        ORDER_STATUSES,
        weights=STATUS_WEIGHTS,
        k=1
    )[0]

    payment_status = get_payment_status(order_status)

    order_date = random_order_date()

    orders.append(
        {
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": order_status,
            "payment_status": payment_status,

            # Will be updated after generating order_items
            "total_before_tax": 0.0,
            "tax_amount": 0.0,
            "total_amount": 0.0
        }
    )

# ==========================
# Save CSV
# ==========================

orders_df = pd.DataFrame(orders)

orders_df.to_csv(
    "data/generated/orders.csv",
    index=False
)

print(f"✅ Generated {len(orders_df)} orders.")