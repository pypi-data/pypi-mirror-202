from BibliotecaRIT.Sources.entidades.Projeto import Projeto
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoCaminho import PreProcessamentoCaminho
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoCodigoHTML import PreProcessamentoCodigoHTML
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoCodigoMarkdown import PreProcessamentoCodigoMarkdown
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoEmoji import PreProcessamentoEmoji
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoEspacos import PreProcessamentoEspacos
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoNumero import PreProcessamentoNumero
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoImagem import PreProcessamentoImagem
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoPontuacao import PreProcessamentoPontuacao
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoURL import PreProcessamentoURL
from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoVersao import PreProcessamentoVersao


class ControladoraPreProcessamento:
    #Alterar a sequência pode alterar o resultado do pré-processamento
    _estrategias = [
        PreProcessamentoEmoji, 
        PreProcessamentoImagem,
        PreProcessamentoCodigoHTML, 
        PreProcessamentoCodigoMarkdown, 
        PreProcessamentoVersao,
        PreProcessamentoURL,
        PreProcessamentoCaminho, 
        PreProcessamentoNumero, 
        PreProcessamentoPontuacao,
        PreProcessamentoEspacos,
    ]

    @classmethod
    def processar(cls, projeto: Projeto) -> Projeto:
        for topico in projeto.topicos:
            for comentario in topico.listaComentarios:
                for estrategia in cls._estrategias:
                    if estrategia.contem(comentario.mensagem):
                        tag = estrategia.getTag()
                        comentario.addTag(tag) if tag is not None else None
                        comentario.mensagem = estrategia.remover(
                            comentario.mensagem)
        return projeto

    # @classmethod
    # def remover(cls, string: str):
    #     for estrategia in cls._estrategias:
    #         if estrategia.contem(string):
    #             tag = estrategia.getTag()
    #             print("add") if tag is not None else None
    #             string = estrategia.remover(string)
    #     return string
