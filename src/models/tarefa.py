import uuid
from datetime import date


class Tarefa:
    TIPOS_VALIDOS = ("Prova", "Entrega", "Trabalho", "Lista")

    def __init__(self, titulo, data_entrega, tipo, descricao=""):
        self._id = uuid.uuid4().hex[:8]
        self.titulo = titulo
        self.tipo = tipo
        self.data_entrega = data_entrega
        self.descricao = descricao
        self._concluida = False

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor.strip():
            raise ValueError("Título inválido.")
        self._titulo = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if valor not in Tarefa.TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo inválido. Use um dos: {', '.join(Tarefa.TIPOS_VALIDOS)}."
            )
        self._tipo = valor

    @property
    def data_entrega(self):
        return self._data_entrega

    @data_entrega.setter
    def data_entrega(self, valor):
        self._data_entrega = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = valor

    @property
    def concluida(self):
        return self._concluida

    @concluida.setter
    def concluida(self, valor: bool):
        """Permite alterar o status de conclusão diretamente (True/False)."""
        self._concluida = bool(valor)

    def marcar_concluida(self):
        self._concluida = True

    def marcar_pendente(self):
        self._concluida = False

    @property
    def esta_atrasada(self):
        if self._concluida:
            return False
        return date.today() > self._data_entrega

    def __str__(self):
        status = "Concluída" if self._concluida else "Pendente"
        return (
            f"[{self._tipo}] {self._titulo} | "
            f"Entrega: {self._data_entrega.strftime('%d/%m/%Y')} | {status}"
        )