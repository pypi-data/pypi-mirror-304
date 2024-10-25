from .aws_db import AWSRDSConnection
from .local_db import LocalDBConnection

def create_db_connection(service, host, user, password, database, port=3306, region=None):
    if service not in ['local', 'aws', 'azure', 'gcp']:
        raise ValueError(f"Unsupported cloud provider: '{service}'. Supported providers: aws, azure, gcp, local")

    if service == "local":
        return LocalDBConnection(host, user, password, database, port)
    elif service == "aws":
        if not region:
            raise ValueError("Region is required for AWS connection.")
        return AWSRDSConnection(host, user, database, region, port)
    else:
        raise ValueError("Unsupported service type. Use 'local', 'aws', 'azure', 'gcp'.")


