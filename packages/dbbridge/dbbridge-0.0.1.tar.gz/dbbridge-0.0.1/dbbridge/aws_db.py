import pymysql
import boto3
import time

class AWSRDSConnection:
    db_connection = None  

    def __init__(self, host, user, database, region, port):
        self.host = host
        self.user = user
        self.database = database
        self.region = region
        self.port = port

    def create_connection_token(self):
        """
        Generate an authentication token for AWS RDS (temporary password).
        """
        client = boto3.client('rds', region_name=self.region)
        token = client.generate_db_auth_token(
            DBHostname=self.host,
            Port=self.port,
            DBUsername=self.user,
            Region=self.region
        )
        return token

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
                self.db_connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.create_connection_token(),
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
                time.sleep(retry_delay)  

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                raise  # Re-raise unexpected exceptions for debugging

        # Exhausted retries, raise the last encountered OperationalError
        raise pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")

