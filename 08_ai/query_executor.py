import os

from dotenv import load_dotenv
from databricks import sql


load_dotenv()


def execute_query(query):

    connection = sql.connect(
        server_hostname=os.getenv(
            "DATABRICKS_HOST"
        ),
        http_path=os.getenv(
            "DATABRICKS_HTTP_PATH"
        ),
        access_token=os.getenv(
            "DATABRICKS_TOKEN"
        )
    )

    cursor = connection.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    connection.close()

    return rows