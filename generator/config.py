from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    # ==========================================
    # Project Paths
    # ==========================================

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    DATA_DIR = PROJECT_ROOT / "data"
    GENERATED_DIR = DATA_DIR / "generated"
    OLD_DATA_DIR = DATA_DIR / "old"

    # ==========================================
    # Output CSV Files
    # ==========================================

    CATEGORIES_FILE = GENERATED_DIR / "categories.csv"
    BRANDS_FILE = GENERATED_DIR / "brands.csv"
    PRODUCTS_FILE = GENERATED_DIR / "products.csv"
    SELLERS_FILE = GENERATED_DIR / "sellers.csv"
    SELLER_PRODUCTS_FILE = GENERATED_DIR / "seller_products.csv"
    WAREHOUSES_FILE = GENERATED_DIR / "warehouses.csv"
    INVENTORY_FILE = GENERATED_DIR / "warehouse_inventory.csv"
    CUSTOMERS_FILE = GENERATED_DIR / "customers.csv"
    RETURN_REASONS_FILE = GENERATED_DIR / "return_reasons.csv"

    # ==========================================
    # Dataset Sizes
    # ==========================================

    NUM_CATEGORIES = 50
    NUM_BRANDS = 30
    NUM_PRODUCTS = 1000
    NUM_SELLERS = 300
    NUM_WAREHOUSES = 30
    NUM_CUSTOMERS = 10000

    # ==========================================
    # Marketplace Rules
    # ==========================================

    SELLERS_PER_PRODUCT = (3, 7)
    WAREHOUSES_PER_SELLER_PRODUCT = (1, 3)

    MIN_STOCK = 20
    MAX_STOCK = 500

    MIN_DISCOUNT = 5
    MAX_DISCOUNT = 40

    COUNTRY = "India"

    RANDOM_SEED = 42