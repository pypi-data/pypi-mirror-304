# sql_profiler/db_connection.py
import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        """
        Initializes the database connection with user-provided parameters.

        :param host: The database server's host (e.g., 'localhost')
        :param user: The username used for the database connection
        :param password: The password for the database user
        :param database: The database name to connect to
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establishes the database connection using the provided parameters."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Connected to the database.")

    def disconnect(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")
