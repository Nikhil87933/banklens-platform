from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

print("Starting BankLens Reset")


# -----------------------
# DATA QUALITY TABLES
# -----------------------

spark.sql("""
DELETE FROM banklens.data_quality.pipeline_control
""")

spark.sql("""
TRUNCATE TABLE banklens.data_quality.pipeline_audit_log
""")

spark.sql("""
TRUNCATE TABLE banklens.data_quality.pipeline_metrics
""")

spark.sql("""
TRUNCATE TABLE banklens.data_quality.schema_change_log
""")

print("Data Quality Tables Cleared")


# -----------------------
# BRONZE TABLES
# -----------------------

bronze_tables = [
    "brz_merchant_reference",
    "brz_market_rates",
    "brz_customer_master",
    "brz_account_master",
    "brz_loan_master",
    "brz_product_holdings",
    "brz_transaction_fact",
    "brz_card_transaction_fact",
    "brz_account_balance_snapshot",
    "brz_device_events",
    "brz_digital_activity",
    "brz_support_tickets"
]

for table_name in bronze_tables:

    spark.sql(
        f"DROP TABLE IF EXISTS banklens.bronze.{table_name}"
    )

print("Bronze Tables Dropped")


# -----------------------
# SILVER TABLES
# -----------------------

silver_tables = [
    "slv_merchant_reference",
    "slv_market_rates",
    "slv_customer_master",
    "slv_account_master",
    "slv_loan_master",
    "slv_product_holdings",
    "slv_transaction_fact",
    "slv_card_transaction_fact",
    "slv_account_balance_snapshot",
    "slv_device_events",
    "slv_digital_activity",
    "slv_support_tickets"
]

for table_name in silver_tables:

    spark.sql(
        f"DROP TABLE IF EXISTS banklens.silver.{table_name}"
    )

print("Silver Tables Dropped")


# -----------------------
# GOLD TABLES
# -----------------------

gold_tables = [
    "gold_customer_360",
    "gld_loan_portfolio",
    "gld_fraud_features",
    "gld_churn_features",
    "gld_executive_kpis"
]

for table_name in gold_tables:

    spark.sql(
        f"DROP TABLE IF EXISTS banklens.gold.{table_name}"
    )

print("Gold Tables Dropped")

print("Pipeline Reset Complete")