from query_executor import execute_query

rows = execute_query(
    """
    SELECT COUNT(*)
    FROM banklens.ml.churn_predictions
    """
)

print(rows)