class AzureDB:
    def __init__(self, connection_string, environment, hostname, port, username, region, dbname):
        self.connection_string = connection_string
        self.environment = environment
        self.hostname = hostname
        self.port = port
        self.username = username
        self.region = region
        self.dbname = dbname

    def connect(self):
        return f"Connected to Azure DB '{self.dbname}' at {self.hostname}:{self.port} in {self.region} environment."
