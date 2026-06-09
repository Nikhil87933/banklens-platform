CREATE TABLE IF NOT EXISTS banklens.data_quality.pipeline_audit_log (
    run_id STRING,
    pipeline_layer STRING,
    table_name STRING,
    day_number INT,
    source_path STRING,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    source_record_count BIGINT,
    target_record_count BIGINT,
    status STRING,
    error_message STRING
)
USING DELTA;

CREATE TABLE IF NOT EXISTS banklens.data_quality.pipeline_control (
    table_name STRING,
    pipeline_layer STRING,
    last_successful_day INT,
    last_run_at TIMESTAMP,
    total_runs INT
)
USING DELTA;

CREATE TABLE IF NOT EXISTS banklens.data_quality.schema_change_log (
    table_name STRING,
    day_number INT,
    detected_at TIMESTAMP,
    previous_columns STRING,
    current_columns STRING,
    columns_added STRING,
    columns_removed STRING,
    columns_renamed STRING
)
USING DELTA;