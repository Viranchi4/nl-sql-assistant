from nl_sql_assistant.database import get_connection


def get_database_schema() -> str:
    """
    Read tables, columns, data types, primary keys,
    and foreign-key relationships from MySQL.

    Returns the schema as formatted text that can later
    be provided to an LLM.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        database_name = connection.database

        # Get all columns from all tables
        cursor.execute(
            """
            SELECT
                TABLE_NAME,
                COLUMN_NAME,
                COLUMN_TYPE,
                IS_NULLABLE,
                COLUMN_KEY
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
            ORDER BY TABLE_NAME, ORDINAL_POSITION
            """,
            (database_name,),
        )

        columns = cursor.fetchall()

        # Get foreign-key relationships
        cursor.execute(
            """
            SELECT
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = %s
              AND REFERENCED_TABLE_NAME IS NOT NULL
            ORDER BY TABLE_NAME, COLUMN_NAME
            """,
            (database_name,),
        )

        foreign_keys = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    # Create an easy lookup for foreign keys
    foreign_key_map = {
        (fk["TABLE_NAME"], fk["COLUMN_NAME"]): (
            fk["REFERENCED_TABLE_NAME"],
            fk["REFERENCED_COLUMN_NAME"],
        )
        for fk in foreign_keys
    }

    schema_lines = []
    current_table = None

    for column in columns:
        table_name = column["TABLE_NAME"]

        if table_name != current_table:
            if current_table is not None:
                schema_lines.append("")

            schema_lines.append(f"TABLE: {table_name}")
            current_table = table_name

        column_name = column["COLUMN_NAME"]
        column_type = column["COLUMN_TYPE"]

        details = []

        if column["COLUMN_KEY"] == "PRI":
            details.append("PRIMARY KEY")

        foreign_key = foreign_key_map.get((table_name, column_name))

        if foreign_key:
            referenced_table, referenced_column = foreign_key
            details.append(
                f"FOREIGN KEY -> {referenced_table}.{referenced_column}"
            )

        if column["IS_NULLABLE"] == "NO":
            details.append("NOT NULL")

        detail_text = ""

        if details:
            detail_text = " [" + ", ".join(details) + "]"

        schema_lines.append(
            f"  - {column_name}: {column_type}{detail_text}"
        )

    return "\n".join(schema_lines)