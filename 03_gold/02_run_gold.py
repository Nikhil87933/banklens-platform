import uuid

from datetime import datetime

from importlib import import_module

from pyspark.sql import functions as F

from marts.loan_portfolio import build_loan_portfolio
from marts.fraud_features import build_fraud_features
from marts.churn_features import build_churn_features
from marts.executive_kpis import build_executive_kpis

gold_framework = import_module(
    "03_gold.01_gold_framework"
)

run_id = str(
    uuid.uuid4()
)

def build_customer_360(spark):

    customer_df = spark.table(
        "banklens.silver.slv_customer_master"
    )

    account_df = (
        spark.table("banklens.silver.slv_account_master")
        .groupBy("customer_id")
        .agg(
            F.count("*").alias("total_accounts"),
            F.sum("current_balance").alias("total_balance")
        )
    )

    product_df = (
        spark.table("banklens.silver.slv_product_holdings")
        .groupBy("customer_id")
        .agg(
            F.count("*").alias("total_products")
        )
    )

    loan_df = (
        spark.table("banklens.silver.slv_loan_master")
        .groupBy("customer_id")
        .agg(
            F.count("*").alias("total_loans")
        )
    )

    digital_df = (
        spark.table("banklens.silver.slv_digital_activity")
        .groupBy("customer_id")
        .agg(
            F.count("*").alias("digital_sessions")
        )
    )

    ticket_df = (
        spark.table("banklens.silver.slv_support_tickets")
        .groupBy("customer_id")
        .agg(
            F.count("*").alias("support_tickets")
        )
    )

    gold_df = (
        customer_df
        .join(account_df, "customer_id", "left")
        .join(product_df, "customer_id", "left")
        .join(loan_df, "customer_id", "left")
        .join(digital_df, "customer_id", "left")
        .join(ticket_df, "customer_id", "left")
    )

    gold_df = (
        gold_df
        .fillna(0, [
            "total_accounts",
            "total_balance",
            "total_products",
            "total_loans",
            "digital_sessions",
            "support_tickets"
        ])
    )

    gold_df = gold_df.select(
        "customer_id",
        "customer_type",
        "customer_since_date",
        "total_accounts",
        "total_products",
        "total_loans",
        "total_balance",
        "digital_sessions",
        "support_tickets",
        "nps_score",
        "is_churn"
    )

    return gold_df

gold_df = build_customer_360(spark)

(
    gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "banklens.gold.gold_customer_360"
    )
)

row_count = gold_df.count()

gold_framework.register_gold_run(
    mart_name="customer_360",
    run_id=run_id,
    started_at=datetime.now(),
    completed_at=datetime.now(),
    row_count=row_count
)

print("Customer 360 Gold created")
print("Rows =", row_count)

loan_df = build_loan_portfolio(spark)

(
    loan_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "banklens.gold.gld_loan_portfolio"
    )
)

row_count = loan_df.count()

gold_framework.register_gold_run(
    mart_name="loan_portfolio",
    run_id=run_id,
    started_at=datetime.now(),
    completed_at=datetime.now(),
    row_count=row_count
)

print(
    "Loan Portfolio Gold created"
)

print(
    "Rows =",
    loan_df.count()
)

fraud_df = build_fraud_features(spark)

(
    fraud_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "banklens.gold.gld_fraud_features"
    )
)

row_count = fraud_df.count()

gold_framework.register_gold_run(
    mart_name="fraud_features",
    run_id=run_id,
    started_at=datetime.now(),
    completed_at=datetime.now(),
    row_count=row_count
)

churn_df = build_churn_features(spark)

(
    churn_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "banklens.gold.gld_churn_features"
    )
)

row_count = churn_df.count()

gold_framework.register_gold_run(
    mart_name="churn_features",
    run_id=run_id,
    started_at=datetime.now(),
    completed_at=datetime.now(),
    row_count=row_count
)

kpi_df = build_executive_kpis(spark)

(
    kpi_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "banklens.gold.gld_executive_kpis"
    )
)

row_count = kpi_df.count()

gold_framework.register_gold_run(
    mart_name="executive_kpis",
    run_id=run_id,
    started_at=datetime.now(),
    completed_at=datetime.now(),
    row_count=row_count
)