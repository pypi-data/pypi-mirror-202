class DolbyText:
    def __init__(self, path):
        self.path = path
        from pathlib import Path
        Path(path).mkdir(parents=True, exist_ok=True)