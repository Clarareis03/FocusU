
class Disciplina:
    total_disciplinas = 0
    def __init__(self, nome, professor):
        self._nome = nome
        self.professor = professor
        Disciplina.total_disciplinas += 1
    def __del__(self):
        if Disciplina.total_disciplinas > 0: Disciplina.total_disciplinas -= 1

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor.strip(): raise ValueError("Nome inválido.")
        self._nome = valor

    def __str__(self): return f"Disciplina: {self.nome} | Prof: {self.professor}"