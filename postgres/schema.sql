-- ============================================================
-- NovaCart / Enterprise Data Platform — PostgreSQL Schema
-- Built to match the actual CSV headers provided.
-- Order matters: tables with foreign keys must be created AFTER
-- the tables they reference. Run this file top to bottom.
-- ============================================================

-- ---------- Independent dimension tables (no FKs) ----------

CREATE TABLE categories (
    category_id     INTEGER PRIMARY KEY,
    category_name   VARCHAR(100) NOT NULL,
    department      VARCHAR(100) NOT NULL,
    gst_percentage  NUMERIC(5,2) NOT NULL
);

CREATE TABLE brands (
    brand_id        INTEGER PRIMARY KEY,
    brand_name      VARCHAR(100) NOT NULL,
    country         VARCHAR(100),
    founded_year    INTEGER
);

CREATE TABLE sellers (
    seller_id       INTEGER PRIMARY KEY,
    seller_name     VARCHAR(255) NOT NULL,
    city            VARCHAR(100),
    state           VARCHAR(100),
    country         VARCHAR(100),
    seller_rating   NUMERIC(3,1),
    verified        BOOLEAN,
    seller_since    DATE
);

CREATE TABLE warehouses (
    warehouse_id    INTEGER PRIMARY KEY,
    warehouse_name  VARCHAR(255) NOT NULL,
    city            VARCHAR(100),
    state           VARCHAR(100),
    country         VARCHAR(100),
    capacity        INTEGER
);

CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY,
    first_name      VARCHAR(100),
    last_name       VARCHAR(100),
    gender          VARCHAR(20),
    age             INTEGER,
    city            VARCHAR(100),
    state           VARCHAR(100),
    country         VARCHAR(100),
    pincode         VARCHAR(10),   -- VARCHAR, not INTEGER: pincodes can have leading zeros
    member_since    DATE,
    membership      VARCHAR(20)
);

CREATE TABLE return_reasons (
    reason_id       INTEGER PRIMARY KEY,
    reason          VARCHAR(255) NOT NULL,
    refund_type     VARCHAR(20)
);

-- ---------- Tables with FKs into the above ----------

CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY,
    sku             VARCHAR(50) UNIQUE NOT NULL,
    product_name    VARCHAR(255) NOT NULL,
    brand_id        INTEGER REFERENCES brands(brand_id),
    category_id     INTEGER REFERENCES categories(category_id),
    cost_price      NUMERIC(12,2) NOT NULL,
    mrp             NUMERIC(12,2) NOT NULL,
    min_discount    NUMERIC(5,2),
    max_discount    NUMERIC(5,2),
    weight_kg       NUMERIC(8,2),
    launch_year     INTEGER
);

CREATE TABLE seller_products (
    seller_product_id  INTEGER PRIMARY KEY,
    seller_id          INTEGER REFERENCES sellers(seller_id),
    product_id         INTEGER REFERENCES products(product_id),
    selling_price      NUMERIC(12,2) NOT NULL
);

CREATE TABLE warehouse_inventory (
    warehouse_inventory_id  INTEGER PRIMARY KEY,
    warehouse_id            INTEGER REFERENCES warehouses(warehouse_id),
    seller_product_id       INTEGER REFERENCES seller_products(seller_product_id),
    stock_quantity          INTEGER NOT NULL,
    last_updated            DATE
);

-- ---------- Transaction tables ----------

CREATE TABLE orders (
    order_id           INTEGER PRIMARY KEY,
    customer_id         INTEGER REFERENCES customers(customer_id),
    order_date          TIMESTAMP NOT NULL,
    status              VARCHAR(20) NOT NULL,
    payment_status      VARCHAR(20) NOT NULL,
    total_before_tax    NUMERIC(12,2) DEFAULT 0,
    tax_amount          NUMERIC(12,2) DEFAULT 0,
    total_amount        NUMERIC(12,2) DEFAULT 0
);

-- NOTE: order_items.csv wasn't included in what you pasted -- this matches
-- the schema from your earlier progress notes. Double check the column
-- names/types here against your actual generate_order_items.py output
-- before running this file, and adjust if they differ.
CREATE TABLE order_items (
    order_item_id           INTEGER PRIMARY KEY,
    order_id                INTEGER REFERENCES orders(order_id),
    seller_product_id       INTEGER REFERENCES seller_products(seller_product_id),
    warehouse_inventory_id  INTEGER REFERENCES warehouse_inventory(warehouse_inventory_id),
    quantity                INTEGER NOT NULL,
    unit_price              NUMERIC(12,2) NOT NULL,
    gst_percentage          NUMERIC(5,2),
    tax_amount              NUMERIC(12,2),
    subtotal_before_tax     NUMERIC(12,2),
    subtotal_after_tax      NUMERIC(12,2)
);

-- ---------- Live streaming output tables ----------

-- Raw valid events landing straight from Spark (Step 3 of the roadmap)
CREATE TABLE live_orders (
    order_id                INTEGER,
    customer_id             INTEGER,
    seller_product_id       INTEGER,
    warehouse_inventory_id  INTEGER,
    quantity                INTEGER,
    selling_price           NUMERIC(12,2),
    amount                  NUMERIC(12,2),
    status                  VARCHAR(20),
    payment_status          VARCHAR(20),
    timestamp               TIMESTAMP
);

-- Rejected events, so chaos-injection actually proves something (see Step 3 discussion)
CREATE TABLE invalid_orders (
    order_id                INTEGER,
    customer_id             INTEGER,
    seller_product_id       INTEGER,
    warehouse_inventory_id  INTEGER,
    quantity                INTEGER,
    selling_price           NUMERIC(12,2),
    amount                  NUMERIC(12,2),
    status                  VARCHAR(20),
    payment_status          VARCHAR(20),
    timestamp               TIMESTAMP,
    rejection_reason        VARCHAR(255),
    received_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);