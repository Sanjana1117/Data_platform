"""
Creates the PostgreSQL schema and loads your generated CSVs into it, in the
correct dependency order (dimension tables first, then anything with foreign keys).

Usage:
    python load_data.py                # create tables + load data
    python load_data.py --reset        # DROP all known tables first, then recreate + load
                                        # (use this since you said one table needs to change)

Environment variables (defaults shown):
    PG_HOST=localhost  PG_PORT=5432  PG_DB=novacart  PG_USER=postgres  PG_PASSWORD=postgres
    DATA_DIR=../data/generated
"""

import os
import sys
import csv
import argparse
import psycopg2

PG_CONFIG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "novacart"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", "sanjana11"),
}

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data", "generated"))
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")

# Load order matters: a table must come after every table it has a foreign key into.
# (table_name, csv_filename)
LOAD_ORDER = [
    ("categories", "categories.csv"),
    ("brands", "brands.csv"),
    ("sellers", "sellers.csv"),
    ("warehouses", "warehouses.csv"),
    ("customers", "customers.csv"),
    ("return_reasons", "return_reasons.csv"),
    ("products", "products.csv"),
    ("seller_products", "seller_products.csv"),
    ("warehouse_inventory", "warehouse_inventory.csv"),
    ("orders", "orders.csv"),
    ("order_items", "order_items.csv"),
]

# Reverse order, for --reset
DROP_ORDER = [t for t, _ in reversed(LOAD_ORDER)] + ["invalid_orders", "live_orders"]


def reset_schema(conn):
    with conn.cursor() as cur:
        for table in DROP_ORDER:
            print(f"dropping table if exists: {table}")
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
    conn.commit()


def create_schema(conn):
    with open(SCHEMA_FILE) as f:
        schema_sql = f.read()
    with conn.cursor() as cur:
        cur.execute(schema_sql)
    conn.commit()
    print("schema created.")


def load_csv(conn, table_name, csv_path):
    if not os.path.exists(csv_path):
        print(f"  SKIPPED (file not found): {csv_path}")
        return

    with open(csv_path, newline="") as f:
        header = next(csv.reader(f))  # read header row to build explicit column list

    columns_sql = ", ".join(header)
    copy_sql = f"COPY {table_name} ({columns_sql}) FROM STDIN WITH (FORMAT csv, HEADER true)"

    with conn.cursor() as cur, open(csv_path) as f:
        cur.copy_expert(copy_sql, f)
    conn.commit()

    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cur.fetchone()[0]
    print(f"  loaded {table_name:<22} <- {os.path.basename(csv_path):<25} ({count} rows now in table)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="drop all known tables before recreating")
    args = parser.parse_args()

    conn = psycopg2.connect(**PG_CONFIG)

    try:
        if args.reset:
            print("=== resetting schema ===")
            reset_schema(conn)

        print("=== creating schema ===")
        create_schema(conn)

        print("=== loading CSVs ===")
        for table_name, csv_filename in LOAD_ORDER:
            csv_path = os.path.join(DATA_DIR, csv_filename)
            load_csv(conn, table_name, csv_path)

        print("\ndone.")
    except Exception as e:
        conn.rollback()
        print(f"\nERROR: {e}", file=sys.stderr)
        print("Rolled back. Fix the issue above and re-run (use --reset if tables partially exist).")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()