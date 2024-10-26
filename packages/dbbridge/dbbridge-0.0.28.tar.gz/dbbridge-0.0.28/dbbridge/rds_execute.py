import pymysql.cursors
from .db_connection import get_db_connection

def get_operation_from_query(query):
    """
    Determine the SQL operation (e.g., 'select', 'insert', 'update', 'delete') from the query.
    """
    return query.strip().split()[0].lower()

def rds_execute(service, query, params=None, **config):
    """
    Execute a query on the RDS or local database.
    """
    connection = None
    print("Query == > ",query)
    print("params == > ", params)
    try:
        connection_obj = get_db_connection(service, **config)
        connection = connection_obj.get_db_connection()
        print("connection == > ", connection)
        with connection.cursor() as cursor:
            if isinstance(params, list) and all(isinstance(i, (tuple, list)) for i in params):
                print("Executing Many")
                cursor.executemany(query, params)
            else:
                print("Executing One")
                cursor.execute(query, params)

            operation = get_operation_from_query(query)
            if operation in ['insert', 'update', 'delete']:
                print("Committing")
                connection.commit()

            if operation == 'select':
                print("Fetching")
                return cursor.fetchall()

    except pymysql.OperationalError as op_err:
        print(f'Operational Error in DB query: {query}')
        return op_err

    except Exception as e:
        print(f'Error while executing DB query: {query}')
        return e

    finally:
        if connection:
            connection_obj.close_connection()
