class Topico:
    def __init__(self, dataCriacao, titulo, descricao, id=0):
        self._dataCriacao = dataCriacao
        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._listaComentarios = []
        
    def inserirComentarios(self, listaComentarios):
        self._listaComentarios = listaComentarios
        
    @property
    def id(self):
        return self._id
    
    @property
    def titulo(self):
        return self._titulo
    
    @property
    def descricao(self):
        return self._descricao
    
    @property
    def dataCriacao(self):
        return self._dataCriacao
    
    @property
    def listaComentarios(self):
        return self._listaComentarios