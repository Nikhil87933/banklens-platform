from pyspark.sql import functions as F


def build_executive_kpis(spark):

    customer_df = spark.table(
        "banklens.silver.slv_customer_master"
    )

    account_df = spark.table(
        "banklens.silver.slv_account_master"
    )

    loan_df = spark.table(
        "banklens.silver.slv_loan_master"
    )

    digital_df = spark.table(
        "banklens.silver.slv_digital_activity"
    )

    support_df = spark.table(
        "banklens.silver.slv_support_tickets"
    )

    result = spark.createDataFrame(
        [(
            customer_df.count(),
            account_df.count(),
            loan_df.count(),
            account_df.agg(
                F.sum("current_balance")
            ).first()[0],
            loan_df.agg(
                F.sum("outstanding_balance")
            ).first()[0],
            digital_df.count(),
            support_df.count()
        )],
        [
            "total_customers",
            "total_accounts",
            "total_loans",
            "total_deposits",
            "total_loan_book",
            "total_digital_events",
            "total_support_tickets"
        ]
    )

    return result