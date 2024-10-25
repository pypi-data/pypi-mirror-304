from .db_manager import create_db_connection

def get_db_connection(db_type, **config):
    """
    Get a database connection based on the provided configuration.

    :param db_type: Type of the database ('aws' or 'local').
    :param config: Configuration parameters for the database connection.
    :return: A database connection object.
    """
    return create_db_connection(db_type=db_type, **config)
