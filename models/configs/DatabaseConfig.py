class DatabaseConfig:
    def __init__(self,
                 host: str = None,
                 user: str = None,
                 password: str = None,
                 name: str = None,
                 ):
        self.host = host
        self.user = user
        self.password = password
        self.name = name
