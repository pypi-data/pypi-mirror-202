class Logger:  # a silence logger that provide same api as logging.Logger but do nothing
    def __init__(self, _: str):
        self.name = _

    def setLevel(self, _: int):
        pass

    def critical(self, _: str):
        pass

    def warn(self, _: str):
        pass

    def debug(self, _: str):
        pass

    def info(self, _: str):
        pass
