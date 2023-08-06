from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoStrategy import PreProcessamentoStrategy
from BibliotecaRIT.Sources.enums.EnumTag import EnumTag
import re


class PreProcessamentoCaminho(PreProcessamentoStrategy):
    _regExp = '([A-Z]:)?[\/\\\]?([^\s\t\n]+[\/\\\])+([a-zA-z0-9\.\%\-\_])*[\s\t\n]'

    @classmethod
    def contem(cls, string: str) -> bool:
        return True if re.search(cls._regExp,string) is not None else False

    @staticmethod
    def getTag() -> EnumTag:
        return EnumTag.CAMINHO

    @classmethod
    def remover(cls,string:str) -> str:
        return re.sub(cls._regExp,' ',string)
