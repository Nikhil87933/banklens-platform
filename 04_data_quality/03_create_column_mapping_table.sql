CREATE TABLE IF NOT EXISTS
banklens.metadata.column_mapping
(
    table_name STRING,
    column_name STRING,
    target_type STRING,
    format_string STRING,
    is_active BOOLEAN,
    loaded_at TIMESTAMP
)
USING DELTA;