from abc import ABC, abstractmethod

# Classe que serve de modelo de herança.
class UsuarioBase(ABC):
    total_usuarios = 0

    def __init__(self, nome, email):
        self._nome = nome
        self._email = email
        UsuarioBase.total_usuarios += 1

    def __del__(self):
        if UsuarioBase.total_usuarios > 0:
            UsuarioBase.total_usuarios -= 1

    # ENCAPSULAMENTO
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("Email inválido.")
        self._email = valor.strip()

    @abstractmethod
    def exibir_perfil(self):
        pass


class Aluno(UsuarioBase):
    def __init__(self, nome, email, matricula, senha="", foto_b64=None):
        super().__init__(nome, email)
        self.matricula = matricula
        self._senha = senha  # Atributo protegido/privado
        self.foto_b64 = foto_b64

        self.disciplinas = []
        self.rotinas = []

    # --- ENCAPSULAMENTO DA SENHA ---
    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, nova_senha):
        if not nova_senha or len(nova_senha) < 3:
            raise ValueError("A senha deve ter pelo menos 3 caracteres.")
        self._senha = nova_senha

    def verificar_senha(self, senha_digitada: str) -> bool:
        """Valida se a senha digitada confere com a cadastrada."""
        return self._senha == senha_digitada

    def adicionar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)

    def adicionar_rotina(self, rotina):
        self.rotinas.append(rotina)

    def exibir_perfil(self):
        return f"Aluno: {self.nome} | Matrícula: {self.matricula}"

    def calcular_tempo_estudo_recursivo(self, indice=0):
        if indice >= len(self.rotinas):
            return 0

        rotina_atual = self.rotinas[indice]
        tempo_valido = 0

        try:
            tempo_valido = int(rotina_atual.tempo)
        except (ValueError, TypeError):
            print(f" [AVISO]: A rotina '{getattr(rotina_atual, 'atividade', 'desconhecida')}' tem um tempo inválido e foi ignorada.")
            tempo_valido = 0

        return tempo_valido + self.calcular_tempo_estudo_recursivo(indice + 1)

    def obter_tarefas_pendentes(self, sistema) -> list:
        tarefas_pendentes = []
        disciplinas = sistema.disciplinas.values() if isinstance(sistema.disciplinas, dict) else sistema.disciplinas

        for disciplina in disciplinas:
            tarefas = getattr(disciplina, "tarefas", [])
            for tarefa in tarefas:
                concluidade = tarefa.get("concluida", False) if isinstance(tarefa, dict) else getattr(tarefa, "concluida", False)
                if not concluidade:
                    titulo = tarefa.get("titulo", "Sem título") if isinstance(tarefa, dict) else getattr(tarefa, "titulo", "Sem título")
                    data = tarefa.get("data_entrega", "Sem data") if isinstance(tarefa, dict) else getattr(tarefa, "data_entrega", "Sem data")
                    
                    nome_disciplina = getattr(disciplina, "nome", "Disciplina")
                    tarefas_pendentes.append({
                        "disciplina": nome_disciplina,
                        "titulo": titulo,
                        "data_entrega": data
                    })
        return tarefas_pendentes

    def calcular_progresso_estudos(self, sistema) -> float:
        total_tarefas = 0
        concluidas = 0

        disciplinas = sistema.disciplinas.values() if isinstance(sistema.disciplinas, dict) else sistema.disciplinas

        for disciplina in disciplinas:
            tarefas = getattr(disciplina, "tarefas", [])
            for tarefa in tarefas:
                total_tarefas += 1
                concluidade = tarefa.get("concluida", False) if isinstance(tarefa, dict) else getattr(tarefa, "concluida", False)
                if concluidade:
                    concluidas += 1

        if total_tarefas == 0:
            return 0.0

        return round((concluidas / total_tarefas) * 100, 1)

    def atualizar_perfil(self, novo_nome: str = None, novo_email: str = None, nova_foto_b64: str = None, nova_senha: str = None):
        """Atualiza as informações do perfil utilizando setters de POO."""
        if novo_nome and novo_nome.strip():
            self.nome = novo_nome  
            
        if novo_email and novo_email.strip():
            self.email = novo_email

        if nova_foto_b64:
            self.foto_b64 = nova_foto_b64

        if nova_senha and nova_senha.strip():
            self.senha = nova_senha

    # --- MÉTODOS DE SERIALIZAÇÃO JSON ---
    def to_dict(self) -> dict:
        """Converte a instância para dicionário para salvar no JSON."""
        return {
            "nome": self.nome,
            "email": self.email,
            "matricula": self.matricula,
            "senha": self.senha,  # Salva a senha no JSON
            "foto_b64": self.foto_b64,
            "rotinas": [r.to_dict() if hasattr(r, "to_dict") else r for r in self.rotinas]
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Aluno":
        """Instancia um Aluno a partir dos dados do JSON."""
        aluno = cls(
            nome=dados.get("nome", ""),
            email=dados.get("email", ""),
            matricula=dados.get("matricula", ""),
            senha=dados.get("senha", ""),  # Restaura a senha do JSON
            foto_b64=dados.get("foto_b64", None)
        )
        return aluno

    def __str__(self):
        return self.exibir_perfil()