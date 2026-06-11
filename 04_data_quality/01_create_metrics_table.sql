CREATE TABLE IF NOT EXISTS
banklens.data_quality.pipeline_metrics
(
    run_id STRING,

    pipeline_layer STRING,

    table_name STRING,

    source_record_count BIGINT,

    target_record_count BIGINT,

    duplicates_removed BIGINT,

    metric_timestamp TIMESTAMP
)
USING DELTA;