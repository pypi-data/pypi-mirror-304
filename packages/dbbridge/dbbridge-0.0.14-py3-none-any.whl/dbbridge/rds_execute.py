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
    try:
        connection_obj = get_db_connection(service, **config)
        connection = connection_obj.get_db_connection()

        with connection.cursor() as cursor:
            if isinstance(params, list) and all(isinstance(i, (tuple, list)) for i in params):
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params or {})

            operation = get_operation_from_query(query)
            if operation in ['insert', 'update', 'delete']:
                connection.commit()

            if operation == 'select':
                return cursor.fetchall()

    except pymysql.OperationalError as op_err:
        print(f'Operational Error in DB query: {query}')
        return op_err

    except Exception as e:
        print(f'Error in DB query: {query}')
        return e

    finally:
        if connection:
            connection_obj.close_connection()
