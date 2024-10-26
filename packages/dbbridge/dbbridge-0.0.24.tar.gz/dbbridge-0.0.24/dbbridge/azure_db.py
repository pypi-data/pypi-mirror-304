import pyodbc
import time

class AzureSQLConnection:
    def __init__(self, server, user, database, password, port=1433):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db_connection = None

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """
        Establish a connection to the Azure SQL Database with retry logic.
        """
        if self.db_connection and self.db_connection.connected:
            return self.db_connection

        retries = 0
        connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};" \
                    f"Server={self.server},{self.port};" \
                    f"Database={self.database};" \
                    f"UID={self.user};" \
                    f"PWD={self.password};" \
                    f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

        while retries < max_retries:
            try:
                self.db_connection = pyodbc.connect(connection_string)
                print("Connection Successful")
                return self.db_connection

            except pyodbc.OperationalError as e:
                retries += 1
                print(f"OperationalError: {e}. Retrying {retries}/{max_retries}...")
                time.sleep(retry_delay)

        raise pyodbc.OperationalError(f"Failed to connect to the database after {max_retries} retries.")

    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
