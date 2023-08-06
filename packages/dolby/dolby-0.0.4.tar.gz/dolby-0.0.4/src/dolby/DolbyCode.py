from .ConstantsDX import *
from .Constants import *

class DolbyCode:
    def __init__(self, path: str = '.') -> None:
        self.path = path
        from pathlib import Path
        Path(path).mkdir(parents=True, exist_ok=True)

    def make(self, query: str) -> None:
        pass
