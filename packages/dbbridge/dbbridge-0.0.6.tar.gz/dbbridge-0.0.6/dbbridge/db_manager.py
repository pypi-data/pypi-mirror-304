from .aws_db import AWSRDSConnection
from .local_db import LocalDBConnection

def create_db_connection(service, host, user, password, database, port=3306):
    if not service or service not in ['local', 'aws', 'azure', 'gcp']:
        raise ValueError(f"Unsupported cloud provider: '{service}'. Supported providers: aws, azure, gcp, local")
    
    if service == "local":
        if not all([host, user, password, database]):
            raise ValueError("Missing parameters for local database connection: host, user, password, and database are required.")
        return LocalDBConnection(host, user, password, database, port)
    
    elif service == "aws":
        if not all([host, user, database]):
            raise ValueError("Missing parameters for AWS database connection: host, user, and database are required.")
        return AWSRDSConnection(host, user, database, port)
    
    else:
        raise ValueError("Unsupported db_type. Use 'local', 'aws', 'azure', 'gcp'.")
