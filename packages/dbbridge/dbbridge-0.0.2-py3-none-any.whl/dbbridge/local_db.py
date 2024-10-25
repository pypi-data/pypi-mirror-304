import pymysql
import boto3
import time

class LocalDBConnection:
    db_connection = None  

    def __init__(self, host, user, password, database, region, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.region = region
        self.port = port

    def close_connection(self):
        """
        Close the database connection if it exists.
        """
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
            print("Database connection closed.")

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """
        Establish a connection to the database, with retry logic for transient errors.
        
        :param max_retries: Maximum retry attempts for connection.
        :param retry_delay: Delay between retries in seconds.
        :return: A pymysql connection object.
        :raises pymysql.OperationalError: If the connection cannot be established after retries.
        """
        # Reuse open connection if available
        if self.db_connection and self.db_connection.open:
            print("Database connection already open.")
            return self.db_connection

        print("Database connection not found. Attempting to create a new one.")
        retries = 0

        while retries < max_retries:
            try:
                # Use the generated token for AWS, or the direct password for local
                self.db_connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.database,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    ssl={"use": True} 
                )
                print("Database connection established.")
                return self.db_connection

            except pymysql.OperationalError as op_err:
                retries += 1
                print(f"OperationalError encountered. Retry {retries} of {max_retries}. Error: {op_err}")
                time.sleep(retry_delay)  # Wait before retrying

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                raise  # Re-raise unexpected exceptions for debugging

        # Exhausted retries, raise the last encountered OperationalError
        raise pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")
