from .aws_db import AWSRDSConnection
from .local_db import LocalDBConnection

def create_db_connection(service, host, user, password, database, port=3306):

    if service not in ['local', 'aws', 'azure', 'gcp']:
        raise ValueError(f"Unsupported cloud provider: '{service}'. Supported providers: aws, azure, gcp, local")
    
    if service == "local":
        return LocalDBConnection(host, user, password, database, port)
    elif service == "aws":
        return AWSRDSConnection(host, user, database, port)
    else:
        raise ValueError("Unsupported db_type. Use 'local', 'aws', 'azure', 'gcp'.")
