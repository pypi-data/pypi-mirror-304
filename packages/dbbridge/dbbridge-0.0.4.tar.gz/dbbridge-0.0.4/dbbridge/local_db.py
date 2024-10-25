import pymysql
import time

class LocalDBConnection:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.db_connection = None

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """
        Establish a connection to the local database with retry logic.
        """
        if self.db_connection and self.db_connection.open:
            return self.db_connection

        retries = 0
        while retries < max_retries:
            try:
                self.db_connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.database,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                return self.db_connection

            except pymysql.OperationalError:
                retries += 1
                time.sleep(retry_delay)

        raise pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")

    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
