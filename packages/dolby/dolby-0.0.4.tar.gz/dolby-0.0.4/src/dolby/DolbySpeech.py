import os
from googletrans import Translator
from .ConstantsDX import *
from .Constants import *


class DolbySpeech:
    def __init__(self, path: str = '.') -> None:
        self.path = path
        from pathlib import Path
        Path(path).mkdir(parents=True, exist_ok=True)

    def translate(self, query: str, language: Language = Language.ENGLISH) -> str:
        translator = Translator()
        translation = translator.translate(query, dest=language.value)
        return translation.text  # type: ignore

    def speak(self, query: str) -> None:
        os.system(f"say {query}")
