class ApiConfig:
    def __init__(self,
                 name: str = None,
                 is_debug: bool = None,
                 port: int = None):
        self.port = port
        self.is_debug = is_debug
        self.name = name
