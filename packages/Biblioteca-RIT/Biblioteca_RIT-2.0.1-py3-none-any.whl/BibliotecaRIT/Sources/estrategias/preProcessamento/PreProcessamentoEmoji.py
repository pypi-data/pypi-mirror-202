from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoStrategy import PreProcessamentoStrategy
from BibliotecaRIT.Sources.enums.EnumTag import EnumTag
import re


class PreProcessamentoEmoji(PreProcessamentoStrategy):
    _regExp = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    @classmethod
    def contem(cls, string: str) -> bool:
        return True if cls._regExp.search(string) is not None else False

    @staticmethod
    def getTag() -> EnumTag:
        return None

    @classmethod
    def remover(cls,string:str) -> str:
        return cls._regExp.sub(r'', string)
