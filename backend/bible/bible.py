from dotmap import DotMap


class Bible:
    def __init__(self, version: str):
        self.version = version
        self.content = DotMap()
