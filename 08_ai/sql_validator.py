FORBIDDEN_KEYWORDS = [
    "DELETE",
    "DROP",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "MERGE"
]


def validate_sql(sql):

    sql_upper = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in sql_upper:

            raise ValueError(
                f"Forbidden SQL detected: {keyword}"
            )

    if not sql_upper.strip().startswith(
        "SELECT"
    ):

        raise ValueError(
            "Only SELECT statements allowed."
        )

    return True