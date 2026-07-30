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

    # --- HELPER PRIVADO (DRY) -------------------------------------------
    def _obter_todas_tarefas_normalizadas(self) -> list:
        """Extrai, filtra por dono e normaliza todas as tarefas das disciplinas
        matriculadas em dicionários padronizados com datas já validadas.

        Fonte única de verdade consumida por obter_tarefas_pendentes,
        obter_tarefas_atrasadas e calcular_progresso_estudos, evitando que
        os três métodos divirjam entre si (ex.: "tarefas fantasmas").
        """
        from datetime import date, datetime

        tarefas_normalizadas = []

        for disciplina in getattr(self, "disciplinas", []):
            if hasattr(disciplina, "listar_tarefas") and callable(getattr(disciplina, "listar_tarefas")):
                tarefas = disciplina.listar_tarefas()
            else:
                tarefas = getattr(disciplina, "tarefas", getattr(disciplina, "_tarefas", []))
                if isinstance(tarefas, dict):
                    tarefas = list(tarefas.values())

            nome_disc = getattr(disciplina, "nome", "Disciplina") if not isinstance(disciplina, dict) else disciplina.get("nome", "Disciplina")

            for tarefa in tarefas:
                if not tarefa:
                    continue

                # Tarefas representadas apenas por string (legado) não têm dono/data
                if isinstance(tarefa, str):
                    tarefas_normalizadas.append({
                        "disciplina": nome_disc,
                        "titulo": tarefa,
                        "concluida": False,
                        "data_obj": None,
                        "data_fmt": "Sem data",
                    })
                    continue

                # Filtra tarefas que pertencem exclusivamente a outro aluno
                dono = getattr(tarefa, "dono", tarefa.get("dono") if isinstance(tarefa, dict) else None)
                if dono and str(dono).strip() != str(self.matricula).strip():
                    continue

                if isinstance(tarefa, dict):
                    concluida = bool(tarefa.get("concluida", False))
                    titulo = str(tarefa.get("titulo", "Sem título"))
                    data_entrega = tarefa.get("data_entrega")
                else:
                    concluida = bool(getattr(tarefa, "concluida", False))
                    titulo = str(getattr(tarefa, "titulo", "Sem título"))
                    data_entrega = getattr(tarefa, "data_entrega", None)  # getattr simples (bug do double-getattr corrigido)

                # Parsing defensivo de data: aceita date/datetime ou string em 2 formatos
                data_obj = None
                if isinstance(data_entrega, str):
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                        try:
                            data_obj = datetime.strptime(data_entrega, fmt).date()
                            break
                        except ValueError:
                            continue
                elif isinstance(data_entrega, (date, datetime)):
                    data_obj = data_entrega if isinstance(data_entrega, date) else data_entrega.date()

                tarefas_normalizadas.append({
                    "disciplina": nome_disc,
                    "titulo": titulo,
                    "concluida": concluida,
                    "data_obj": data_obj,
                    "data_fmt": data_obj.strftime("%d/%m/%Y") if data_obj else str(data_entrega or "Sem data"),
                })

        return tarefas_normalizadas

    # --- MÉTODOS PÚBLICOS --------------------------------------------------
    def obter_tarefas_pendentes(self, sistema=None) -> list:
        """Retorna as tarefas não concluídas e dentro do prazo (ou sem data definida).

        O parâmetro `sistema` é opcional e existe apenas para compatibilidade
        com chamadas da interface Streamlit (`aluno.obter_tarefas_pendentes(sistema)`).
        """
        from datetime import date
        hoje = date.today()

        pendentes = []
        for t in self._obter_todas_tarefas_normalizadas():
            if t["concluida"]:
                continue
            if not t["data_obj"] or t["data_obj"] >= hoje:
                pendentes.append({
                    "disciplina": t["disciplina"],
                    "titulo": t["titulo"],
                    "data_entrega": t["data_fmt"],
                })
        return pendentes

    def obter_tarefas_atrasadas(self, sistema=None) -> list:
        """Retorna as tarefas não concluídas cuja data de entrega já passou."""
        from datetime import date
        hoje = date.today()

        atrasadas = []
        for t in self._obter_todas_tarefas_normalizadas():
            if not t["concluida"] and t["data_obj"] and t["data_obj"] < hoje:
                atrasadas.append({
                    "disciplina": t["disciplina"],
                    "titulo": t["titulo"],
                    "data_entrega": t["data_fmt"],
                })
        return atrasadas

    def calcular_progresso_estudos(self, sistema=None) -> float:
        """Calcula o percentual de tarefas concluídas do aluno (0 a 100)."""
        tarefas = self._obter_todas_tarefas_normalizadas()
        if not tarefas:
            return 0.0

        concluidas = sum(1 for t in tarefas if t["concluida"])
        return round((concluidas / len(tarefas)) * 100, 1)

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