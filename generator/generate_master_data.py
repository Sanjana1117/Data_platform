import os

FILES = [

    "generate_categories.py",

    "generate_brands.py",

    "generate_products.py",

    "generate_sellers.py",

    "generate_seller_products.py",

    "generate_warehouses.py",

    "generate_inventory.py",

    "generate_customers.py",

    "generate_return_reasons.py"

]

for file in FILES:

    print(f"\nRunning {file}...")

    exit_code = os.system(f"python generator/{file}")

    if exit_code != 0:
        raise RuntimeError(f"{file} failed.")

print("\n🎉 All master data generated successfully!")