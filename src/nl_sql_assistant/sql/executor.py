from nl_sql_assistant.database import get_connection


def execute_query(query: str):
    """
    Execute a SQL query and return the result as a list of dictionaries.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()