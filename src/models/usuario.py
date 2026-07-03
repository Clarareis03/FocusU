from abc import ABC, abstractmethod

# Classe que serve de modelo de herança. Possui atributos
# estáticos de contagem e métodos abstratos herdados.

class UsuarioBase(ABC):
    total_usuarios = 0

    def __init__(self, nome, email):
        self._nome = nome
        self._email = email
        UsuarioBase.total_usuarios += 1

    def __del__(self):
        if UsuarioBase.total_usuarios > 0:
            UsuarioBase.total_usuarios -= 1


    # CONCEITO: ENCAPSULAMENTO
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("Email inválido.")
        self._email = valor


    # CONCEITO: MÉTODO ABSTRATO
    # Força as classes filhas a implementarem sua própria versão.

    @abstractmethod
    def exibir_perfil(self):
        pass


# CONCEITO: HERANÇA
# Classe Aluno estende a classe abstrata UsuarioBase.

class Aluno(UsuarioBase):
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email)
        self.matricula = matricula


        # CONCEITO: ASSOCIAÇÃO
        # Armazena internamente referências de objetos de outras classes.
        self.disciplinas = []
        self.rotinas = []

    def adicionar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)

    def adicionar_rotina(self, rotina):
        self.rotinas.append(rotina)

    def exibir_perfil(self):
        return f"Aluno: {self.nome} | Matrícula: {self.matricula}"

    def __str__(self):
        return self.exibir_perfil()