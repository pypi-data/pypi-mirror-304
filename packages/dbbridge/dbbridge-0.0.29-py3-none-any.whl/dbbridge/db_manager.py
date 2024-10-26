from .local_db import LocalDBConnection
from .aws_db import AWSRDSConnection
from .azure_db import AzureSQLConnection 

def create_db_connection(service, host=None, user=None, password=None, database=None, port=3306, region=None):
    if service not in ['local', 'aws', 'azure', 'gcp']:
        return ValueError(f"Unsupported cloud provider: '{service}'. Supported providers: aws, azure, gcp, local")

    if service == "local":
        return LocalDBConnection(host, user, password, database, port)
    elif service == "aws":
        if not region:
            return ValueError("Region is required for AWS connection.")
        return AWSRDSConnection(host, user, database, region, port)
    elif service == "azure":
        return AzureSQLConnection(host, user, database, password, port)
    else:
        raise ValueError("Unsupported service type. Use 'local', 'aws', 'azure', 'gcp'.")