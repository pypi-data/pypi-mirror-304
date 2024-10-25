import pymysql.cursors
from .db_connection import get_db_connection

def get_operation_from_query(query):
    """
    Determine the SQL operation (e.g., 'select', 'insert', 'update', 'delete') from the query.

    :param query: The SQL query as a string.
    :return: The operation type as a lowercase string.
    """
    if not query:
        raise ValueError("SQL query cannot be None or empty.")
    
    operation = query.strip().split()[0].lower()
    return operation

def rds_execute(service, query, params=None, **config):
    """
    Execute a query on the RDS or local database.

    :param service: Type of the database ('aws' or 'local').
    :param query: The SQL query to execute.
    :param params: Optional parameters for the SQL query.
    :param config: Configuration parameters for the database connection.
    :return: Results for 'select' queries; None otherwise.
    """
    if not service or not query:
        raise ValueError("Both service type and query are required.")

    connection = None
    try:
        # Get the database connection
        connection_obj = get_db_connection(service, **config)
        connection = connection_obj.connect_to_database()
        
        with connection.cursor() as cursor:
            if isinstance(params, list) and all(isinstance(i, (tuple, list)) for i in params):
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params or {})
            
            # Commit for insert, update, or delete operations
            operation = get_operation_from_query(query)
            if operation in ['insert', 'update', 'delete']:
                connection.commit()

            # Return results for select operations
            if operation == 'select':
                return cursor.fetchall()

    except pymysql.OperationalError as op_err:
        print(f'Operational Error in DB query: {query}. Error: {op_err}')

    except Exception as e:
        print(f'Error in DB query: {query}. Error: {e}')

    finally:
        # Close connection if it's open
        if connection:
            connection_obj.close_connection(connection)
