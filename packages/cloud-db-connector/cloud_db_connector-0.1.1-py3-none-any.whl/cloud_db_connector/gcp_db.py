class GCPDB:
    def __init__(self, environment, hostname, port, username, region, dbname):
        self.environment = environment
        self.hostname = hostname
        self.port = port
        self.username = username
        self.region = region
        self.dbname = dbname

    def connect(self):
        return f"Connected to GCP DB '{self.dbname}' at {self.hostname}:{self.port} in {self.region} environment."
