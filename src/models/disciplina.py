from .tarefa import Tarefa


class Disciplina:
    total_disciplinas = 0

    def __init__(self, nome, professor):
        self._nome = nome
        self.professor = professor
        self._tarefas = {}
        Disciplina.total_disciplinas += 1

    def __del__(self):
        if Disciplina.total_disciplinas > 0:
            Disciplina.total_disciplinas -= 1

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor.strip():
            raise ValueError("Nome inválido.")
        self._nome = valor

    def adicionar_tarefa(self, titulo, data_entrega, tipo, descricao=""):
        tarefa = Tarefa(titulo, data_entrega, tipo, descricao)
        self._tarefas[tarefa.id] = tarefa
        return tarefa

    def concluir_tarefa(self, id_tarefa):
        tarefa = self._tarefas.get(id_tarefa)
        if tarefa is None:
            return False
        tarefa.marcar_concluida()
        return True

    def remover_tarefa(self, id_tarefa):
        return self._tarefas.pop(id_tarefa, None) is not None

    def listar_tarefas(self, status=None):
        tarefas = list(self._tarefas.values())
        if status == "pendentes":
            return [t for t in tarefas if not t.concluida]
        if status == "concluidas":
            return [t for t in tarefas if t.concluida]
        return tarefas

    def __str__(self):
        return (
            f"Disciplina: {self.nome} | Prof: {self.professor} | "
            f"Tarefas: {len(self._tarefas)}"
        )