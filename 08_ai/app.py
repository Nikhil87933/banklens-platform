from sql_generator import generate_sql
from sql_validator import validate_sql
from query_executor import execute_query

question = input(
    "Ask BankLens: "
)

sql = generate_sql(question)

validate_sql(sql)

print("\nGenerated SQL:\n")
print(sql)

result_df = execute_query(
    spark,
    sql
)

print("\nQuery Result:\n")

result_df.show(truncate=False)