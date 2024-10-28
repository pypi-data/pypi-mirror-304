from .local_db import LocalDBConnection
from .aws_db import AWSRDSConnection
from .azure_db import AzureSQLConnection 
from .gcp_db import GCPMySQLConnection

def create_db_connection(service, host=None, user=None, password=None, database=None, port=3306, region=None):
    """
    Establishes a database connection based on the specified cloud provider or local setup.

    This function returns a connection object for either a local database or a cloud database service (AWS, Azure, GCP)
    based on the input parameters. The connection object returned will depend on the `service` parameter and the 
    corresponding required fields for each provider.

    Parameters:
        service (str): Specifies the type of database connection to establish. 
                       Must be one of ['local', 'aws', 'azure', 'gcp'].
        host (str, optional): The hostname or IP address of the database server.
        user (str, optional): Username for authentication to the database.
        password (str, optional): Password for authentication to the database.
        database (str, optional): Name of the database to connect to.
        port (int, optional): The port number for the database connection. Defaults to 3306.
        region (str, optional): The AWS region for an RDS connection; required if `service` is 'aws'.

    Returns:
        Database connection object (LocalDBConnection, AWSRDSConnection, AzureSQLConnection, or GCPMySQLConnection):
        Returns an instance of the appropriate database connection class based on the `service` parameter.
    
    Raises:
        ValueError: If an unsupported `service` value is provided or required parameters are missing.
                    - Raises if `service` is not in ['local', 'aws', 'azure', 'gcp'].
                    - Raises if `service` is 'aws' and `region` is not provided.

    Examples:
        >>> # Establish a local database connection
        >>> connection = create_db_connection('local', host='localhost', user='user', password='pass', database='test_db')

        >>> # Establish an AWS RDS connection
        >>> connection = create_db_connection('aws', host='db-instance.123456789012.us-east-1.rds.amazonaws.com', 
                                              user='admin', database='test_db', region='us-east-1')

    """
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
    elif service == "gcp":
        return GCPMySQLConnection(host, user, password, database, port)
    else:
        raise ValueError("Unsupported service type. Use 'local', 'aws', 'azure', 'gcp'.")