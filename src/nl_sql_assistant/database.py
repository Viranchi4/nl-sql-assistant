import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """
    Create and return a connection to the MySQL database
    using configuration stored in the .env file.
    """

    connection = mysql.connector.connect(
        host=os.getenv("SA_DB_HOST"),
        port=int(os.getenv("SA_DB_PORT", "3306")),
        user=os.getenv("SA_DB_USER"),
        password=os.getenv("SA_DB_PASSWORD"),
        database=os.getenv("SA_DB_NAME"),
    )

    return connection