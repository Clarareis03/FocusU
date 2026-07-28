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
            tempo_valido = int(getattr(rotina_atual, "tempo", 0))
        except (ValueError, TypeError, AttributeError):
            print(f" [AVISO]: A rotina '{getattr(rotina_atual, 'atividade', 'desconhecida')}' tem um tempo inválido e foi ignorada.")
            tempo_valido = 0

        return tempo_valido + self.calcular_tempo_estudo_recursivo(indice + 1)

    def obter_tarefas_pendentes(self) -> list:
        tarefas_pendentes = []
        
        # Recupera as disciplinas do próprio aluno (removida a busca global)
        disciplinas = self.disciplinas

        for disciplina in disciplinas:
            if hasattr(disciplina, "listar_tarefas") and callable(getattr(disciplina, "listar_tarefas")):
                tarefas = disciplina.listar_tarefas()
            else:
                tarefas = getattr(disciplina, "tarefas", getattr(disciplina, "_tarefas", []))
                if isinstance(tarefas, dict):
                    tarefas = list(tarefas.values())

            for tarefa in tarefas:
                if not tarefa:
                    continue

                concluida = False
                titulo = "Sem título"
                data = "Sem data"

                if isinstance(tarefa, dict):
                    concluida = bool(tarefa.get("concluida", False))
                    titulo = str(tarefa.get("titulo", "Sem título"))
                    data = str(tarefa.get("data_entrega", "Sem data"))
                elif isinstance(tarefa, str):
                    titulo = tarefa
                else:
                    concluida = bool(getattr(tarefa, "concluida", False))
                    titulo = str(getattr(tarefa, "titulo", "Sem título"))
                    data = str(getattr(tarefa, "data_entrega", "Sem data"))

                if not concluida:
                    nome_disciplina = getattr(disciplina, "nome", "Disciplina") if not isinstance(disciplina, dict) else disciplina.get("nome", "Disciplina")
                    
                    tarefas_pendentes.append({
                        "disciplina": nome_disciplina,
                        "titulo": titulo,
                        "data_entrega": data
                    })
        return tarefas_pendentes

    def calcular_progresso_estudos(self):
        # 1. Recupera as disciplinas do próprio aluno (removida a busca global)
        disciplinas = self.disciplinas

        if not disciplinas:
            return 0.0

        total_tarefas = 0
        tarefas_concluidas = 0

        # 2. Percorre as disciplinas do aluno calculando o progresso
        for d in disciplinas:
            if hasattr(d, "listar_tarefas") and callable(getattr(d, "listar_tarefas")):
                tarefas = d.listar_tarefas()
            elif hasattr(d, "_tarefas"):
                t_attr = getattr(d, "_tarefas")
                tarefas = list(t_attr.values()) if isinstance(t_attr, dict) else t_attr
            elif isinstance(d, dict):
                t_attr = d.get("_tarefas", d.get("tarefas", []))
                tarefas = list(t_attr.values()) if isinstance(t_attr, dict) else t_attr
            else:
                tarefas = []

            for t in tarefas:
                if not t:
                    continue
                
                total_tarefas += 1
                
                is_concluida = False
                try:
                    if isinstance(t, dict):
                        is_concluida = bool(t.get("concluida", False))
                    elif not isinstance(t, str):
                        is_concluida = bool(getattr(t, "concluida", False))
                except Exception:
                    is_concluida = False

                if is_concluida:
                    tarefas_concluidas += 1

        if total_tarefas == 0:
            return 0.0

        return round((tarefas_concluidas / total_tarefas) * 100, 1)

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
            "senha": self.senha,
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
            senha=dados.get("senha", ""),
            foto_b64=dados.get("foto_b64", None)
        )
        return aluno

    def __str__(self):
        return self.exibir_perfil()