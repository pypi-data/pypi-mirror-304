class AWSDB:
    def __init__(self, environment, hostname, port, username, region, dbname):
        self.environment = environment
        self.hostname = hostname
        self.port = port
        self.username = username
        self.region = region
        self.dbname = dbname

    def connect(self):
        return f"Connected to AWS DB '{self.dbname}' at {self.hostname}:{self.port} in {self.region} environment."
