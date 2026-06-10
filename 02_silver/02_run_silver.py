from importlib import import_module

framework = import_module(
    "02_silver.01_silver_framework"
)

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

for table_name in TABLES:

    framework.process_table(
        table_name
    )

print(
    "Silver load complete"
)