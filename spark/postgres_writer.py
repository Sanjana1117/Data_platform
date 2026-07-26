# ==========================================
# PostgreSQL Configuration
# ==========================================

JDBC_URL = "jdbc:postgresql://postgres:5432/enterprise_db"

JDBC_OPTIONS = {
    "url": JDBC_URL,
    "user": "postgres",
    "password": "sanjana11",
    "driver": "org.postgresql.Driver"
}


# ==========================================
# Write Streams to PostgreSQL
# ==========================================

def write_to_postgres(raw_df, enriched_df, invalid_df, batch_id):

    print(f"\n========== Batch {batch_id} ==========")

    raw_count = raw_df.count()
    enriched_count = enriched_df.count()
    invalid_count = invalid_df.count()

    total = raw_count

    print(f"Total Events     : {total}")
    print(f"Raw Events     : {raw_count}")
    print(f"Valid Orders   : {enriched_count}")
    print(f"Invalid Orders : {invalid_count}")

    if total > 0:
        print(f"Success Rate     : {(enriched_count / total) * 100:.2f}%")

    # --------------------------------------
    # Raw Orders (Bronze Layer)
    # --------------------------------------

    if raw_count > 0:

        raw_df.write \
            .format("jdbc") \
            .options(**JDBC_OPTIONS) \
            .option("dbtable", "live_orders") \
            .mode("append") \
            .save()

        print("live_orders updated")

    # --------------------------------------
    # Enriched Valid Orders (Silver Layer)
    # --------------------------------------

    if enriched_count > 0:

        enriched_df.write \
            .format("jdbc") \
            .options(**JDBC_OPTIONS) \
            .option("dbtable", "enriched_live_orders") \
            .mode("append") \
            .save()

        print(" enriched_live_orders updated")

    # --------------------------------------
    # Invalid Orders (Dead Letter Queue)
    # --------------------------------------

    if invalid_count > 0:

        invalid_df.write \
            .format("jdbc") \
            .options(**JDBC_OPTIONS) \
            .option("dbtable", "invalid_orders") \
            .mode("append") \
            .save()

        print("invalid_orders updated")