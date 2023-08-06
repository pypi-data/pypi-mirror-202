from BibliotecaRIT.Sources.enums.EnumTag import EnumTag


class Comentario:
    def __init__(self, id, loginAutor, mensagem, data):
        self._id = id
        self._loginAutor = loginAutor
        self._mensagem = mensagem
        self._data = data
        self._relevancia = 0
        self._tags = [None,None,None,None]
        
    def inserirRelevanciaTematica(self, relevancia):
        self._relevancia = relevancia
    
    def addTag(self,tag:EnumTag):
        self._tags[tag.value] = 1
        
    @property
    def relevancia(self):
        return self._relevancia
    
    @property
    def mensagem(self):
        return self._mensagem
    
    @property
    def data(self):
        return self._data
    
    @property
    def loginAutor(self):
        return self._loginAutor
    
    @property
    def id(self):
        return self._id
    @property
    def tags(self):
        return self._tags