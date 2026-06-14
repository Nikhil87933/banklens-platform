from pyspark.sql import functions as F


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