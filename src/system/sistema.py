import unicodedata
from models.usuario import Aluno, UsuarioBase
from models.disciplina import Disciplina
from models.rotina import Rotina
from models.postagem import Postagem
from models.evento import Evento

# CLASSE GERENCIADORA
# Centraliza métodos de controle

class SistemaFocusU:
    def __init__(self):
        # Tabelas Hash (Dicionários) para busca e validação O(1)
        self.alunos_por_matricula = {}
        self.alunos_por_email = {}
        self.disciplinas_por_nome = {}
        
        # Postagens e Eventos continuam como listas (ordem de feed importa)
        self.postagens = []
        self.eventos = []

    def _normalizar_chave(self, texto: str) -> str:
        """
        Remove acentos, converte para minúsculas e remove espaços extras.
        Exemplo: "Análise de Dados  " -> "analise de dados"
        """
        if not texto:
            return ""
        # Decompõe caracteres acentuados (ex: 'á' vira 'a' + '´')
        nfkd = unicodedata.normalize('NFD', texto)
        # Filtra mantendo apenas letras/números sem os acentos
        texto_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return texto_sem_acento.lower().strip()

    def adicionar_aluno(self, aluno):
        # Normalização de e-mail e matrícula para evitar duplicidades por maiúsculas/espaços
        mat_chave = aluno.matricula.strip()
        email_chave = aluno.email.lower().strip()

        if mat_chave in self.alunos_por_matricula:
            raise ValueError(f"Erro: A matrícula '{aluno.matricula}' já está cadastrada.")
        if email_chave in self.alunos_por_email:
            raise ValueError(f"Erro: O e-mail '{aluno.email}' já está em uso.")
            
        # Adiciona nos dois índices
        self.alunos_por_matricula[mat_chave] = aluno
        self.alunos_por_email[email_chave] = aluno

    # Exclusão segura
    def remover_aluno(self, aluno):
        # Quebra de associação direta mantendo integridade da postagem (Anonimização)
        for post in self.postagens:
            if post.autor == aluno:
                post.autor = None

        if hasattr(aluno, 'rotinas'):
            for rotina in aluno.rotinas:
                rotina.__del__()
                
        if hasattr(aluno, 'disciplinas'):
            for disc in aluno.disciplinas:
                chave_disc = self._normalizar_chave(disc.nome)
                if chave_disc in self.disciplinas_por_nome:
                    del self.disciplinas_por_nome[chave_disc]
                disc.__del__()

        # Remoção O(1) do aluno dos dicionários
        mat_chave = aluno.matricula.strip()
        email_chave = aluno.email.lower().strip()

        if mat_chave in self.alunos_por_matricula:
            del self.alunos_por_matricula[mat_chave]
        if email_chave in self.alunos_por_email:
            del self.alunos_por_email[email_chave]

        aluno.__del__()

    def adicionar_disciplina_global(self, d):
        # Chave normalizada para comparação O(1) insensível a acentos/caixa
        chave_nome = self._normalizar_chave(d.nome)

        if chave_nome in self.disciplinas_por_nome:
            raise ValueError(f"A disciplina '{d.nome}' (ou similar) já existe no sistema.")
        
        # Guarda o objeto indexado pela chave limpa
        self.disciplinas_por_nome[chave_nome] = d

    def adicionar_postagem(self, p): 
        self.postagens.append(p)
        
    def adicionar_evento(self, e): 
        self.eventos.append(e)

    def listar_alunos(self):
        print("\n===== ALUNOS =====")
        if not self.alunos_por_matricula: 
            print("Nenhum cadastrado.")
            return
            
        for a in self.alunos_por_matricula.values():
            print(a)
            if hasattr(a, 'disciplinas') and a.disciplinas:
                print("  Disciplinas Matriculadas:", [d.nome for d in a.disciplinas])
            if hasattr(a, 'rotinas') and a.rotinas:
                print("  Plano de Rotinas:")
                for r in a.rotinas:
                    print(f"   - {r}")

    def exibir_feed(self):
        print("\n===== FEED FOCUS U =====")
        feed = self.postagens + self.eventos
        if not feed:
            print("Feed vazio.")
            return
        for item in feed:
            print(item.publicar())
            print("-" * 40)

    def estatisticas(self):
        print("\n===== ESTATÍSTICAS =====")
        print(f"Alunos Ativos: {UsuarioBase.total_usuarios}")
        print(f"Postagens Ativas: {Postagem.total_postagens}")
        print(f"Disciplinas no App: {Disciplina.total_disciplinas}")
        print(f"Rotinas Existentes: {Rotina.total_rotinas}")