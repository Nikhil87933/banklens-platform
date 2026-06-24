def get_schema_files(question):

    question = question.lower()

    if "high risk" in question:
        return [
            "churn_predictions.txt"
        ]

    if "risk" in question:
        return [
            "churn_predictions.txt"
        ]

    if "predicted churn" in question:
        return [
            "churn_predictions.txt"
        ]

    if "loan" in question:
        return [
            "gld_loan_portfolio.txt"
        ]

    if "churn" in question:
        return [
            "churn_predictions.txt",
            "gld_churn_features.txt"
        ]

    if "customer" in question:
        return [
            "gold_customer_360.txt",
            "gld_executive_kpis.txt"
        ]

    return [
        "gld_executive_kpis.txt"
    ]