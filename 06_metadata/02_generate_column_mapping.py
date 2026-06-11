from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

TABLES = [

    "merchant_reference",
    "market_rates",

    "customer_master",
    "account_master",
    "loan_master",
    "product_holdings",

    "transaction_fact",
    "card_transaction_fact",
    "account_balance_snapshot",

    "device_events",
    "digital_activity",
    "support_tickets"
]

rows = []

for table_name in TABLES:

    print(
        f"Scanning {table_name}"
    )

    df = spark.table(
        f"banklens.bronze.brz_{table_name}"
    )

    for column_name in df.columns:

        if column_name.startswith("_"):
            continue

        rows.append(
            (
                table_name,
                column_name,
                "STRING",
                "",
                True
            )
        )

metadata_df = spark.createDataFrame(
    rows,
    [
        "table_name",
        "column_name",
        "target_type",
        "format_string",
        "is_active"
    ]
)

print(
    f"Total Rows = {metadata_df.count()}"
)

metadata_df.show(
    100,
    truncate=False
)
