# ==========================================
# Write Batch to PostgreSQL
# ==========================================

def write_to_postgres(batch_df, batch_id):

    print(f"\n========== Batch {batch_id} ==========")

    batch_df.show(truncate=False)

    (
        batch_df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://postgres:5432/postgres")
        .option("dbtable", "live_orders")
        .option("user", "postgres")
        .option("password", "sanjana11")
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

    print("Batch written successfully.")