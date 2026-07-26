from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_data_quality_analytics(
    valid_df: DataFrame,
    invalid_df: DataFrame
) -> DataFrame:
    """
    Build data quality metrics for the current batch.

    Parameters
    ----------
    valid_df : DataFrame
        DataFrame containing all valid records.

    invalid_df : DataFrame
        DataFrame containing all invalid records.

    Returns
    -------
    DataFrame
        Single-row DataFrame containing batch quality metrics.
    """

    # Record counts
    valid_count = valid_df.count()
    invalid_count = invalid_df.count()

    total_events = valid_count + invalid_count

    # Success rate
    success_rate = (
        round((valid_count / total_events) * 100, 2)
        if total_events > 0
        else 0.0
    )

    # Failure rate
    failure_rate = (
        round((invalid_count / total_events) * 100, 2)
        if total_events > 0
        else 0.0
    )

    # Error breakdown
    if invalid_count > 0:
        error_summary = (
            invalid_df.groupBy("reason")
            .count()
            .orderBy(F.desc("count"))
            .withColumn(
                "error_summary",
                F.concat(
                    F.col("reason"),
                    F.lit(": "),
                    F.col("count")
                )
            )
            .agg(
                F.concat_ws(", ", F.collect_list("error_summary"))
                .alias("error_summary")
            )
            .first()["error_summary"]
        )
    else:
        error_summary = "No validation errors"

    metrics = [
        (
            total_events,
            valid_count,
            invalid_count,
            success_rate,
            failure_rate,
            error_summary
        )
    ]

    columns = [
        "total_events",
        "valid_events",
        "invalid_events",
        "success_rate",
        "failure_rate",
        "error_summary"
    ]

    return valid_df.sparkSession.createDataFrame(metrics, columns)