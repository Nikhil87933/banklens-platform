CREATE TABLE IF NOT EXISTS
banklens.data_quality.pipeline_metrics
(
    run_id STRING,

    pipeline_layer STRING,

    table_name STRING,

    status STRING,

    source_record_count BIGINT,

    target_record_count BIGINT,

    duplicates_removed BIGINT,

    duplicate_percentage DOUBLE,

    processing_time_seconds DOUBLE,

    rows_per_second DOUBLE,

    metric_timestamp TIMESTAMP
)
USING DELTA;