class BaseConfig:
    """Base config abstract class"""

    def __init__(self) -> None:
        self.testcases = []
        self.model = ""
        self.logger = ""


base = BaseConfig()
