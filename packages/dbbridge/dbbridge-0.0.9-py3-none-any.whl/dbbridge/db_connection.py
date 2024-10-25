from .db_manager import create_db_connection

def get_db_connection(service, **config):
    """
    Get a database connection based on the provided configuration.

    :param service: Type of the database ('aws' or 'local').
    :param config: Configuration parameters for the database connection.
    :return: A database connection object.
    """
    return create_db_connection(service=service, **config)
