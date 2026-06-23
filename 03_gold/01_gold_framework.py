from pyspark.sql import SparkSession

from importlib import import_module

spark = SparkSession.builder.getOrCreate()

audit_utils = import_module(
    "99_utils.audit_utils"
)

metrics_utils = import_module(
    "99_utils.metrics_utils"
)


def register_gold_run(
    mart_name: str,
    run_id: str,
    started_at,
    completed_at,
    row_count: int
):

    audit_utils.write_audit_log(
        run_id=run_id,
        pipeline_layer="GOLD",
        table_name=mart_name,
        day_number=0,
        source_path="SILVER_TABLES",
        started_at=started_at,
        completed_at=completed_at,
        source_record_count=row_count,
        target_record_count=row_count,
        status="SUCCESS",
        error_message=""
    )

    audit_utils.write_control_record(
        table_name=mart_name,
        pipeline_layer="GOLD",
        day_number=0
    )

    processing_time_seconds = (
        completed_at - started_at
    ).total_seconds()

    if processing_time_seconds > 0:

        rows_per_second = round(
            row_count /
            processing_time_seconds,
            2
        )

    else:

        rows_per_second = 0

    metrics_utils.write_pipeline_metrics(
        run_id=run_id,
        pipeline_layer="GOLD",
        table_name=mart_name,
        status="SUCCESS",
        source_record_count=row_count,
        target_record_count=row_count,
        duplicates_removed=0,
        duplicate_percentage=0,
        processing_time_seconds=processing_time_seconds,
        rows_per_second=rows_per_second
    )