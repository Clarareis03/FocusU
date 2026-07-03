from models.usuario import Aluno
from models.disciplina import Disciplina
from models.rotina import Rotina
from models.postagem import Postagem
from models.evento import Evento

# CLASSE GEERENCIADORA
# Centraliza métodos de controle

class SistemaFocusU:
    def __init__(self):
        self.alunos = []
        self.disciplinas_globais = []
        self.postagens = []
        self.eventos = []

    def adicionar_aluno(self, aluno): self.alunos.append(aluno)

    # Exclusão segura
    def remover_aluno(self, aluno):
        # Quebra de associação direta mantendo integridade da postagem (Anonimização)
        for post in self.postagens:
            if post.autor == aluno:
                post.autor = None

        for rotina in aluno.rotinas:
            rotina.__del__()
        for disc in aluno.disciplinas:
            if disc in self.disciplinas_globais:
                self.disciplinas_globais.remove(disc)
            disc.__del__()

        if aluno in self.alunos:
            self.alunos.remove(aluno)
            aluno.__del__()

    def adicionar_disciplina_global(self, d): self.disciplinas_globais.append(d)
    def adicionar_postagem(self, p): self.postagens.append(p)
    def adicionar_evento(self, e): self.eventos.append(e)

    def listar_alunos(self):
        print("\n===== ALUNOS =====")
        if not self.alunos: print("Nenhum cadastrado.")
        for a in self.alunos:
            print(a)
            if a.disciplinas:
                print("  Disciplinas Matriculadas:", [d.nome for d in a.disciplinas])
            if a.rotinas:
                print("  Plano de Rotinas:")
                for r in a.rotinas:
                    print(f"   - {r}")


    # CONCEITO: EXECUÇÃO DO POLIMORFISMO
    # O motor itera sobre uma coleção genérica de objetos 'Publicavel'
    # executando a chamada polimórfica única sem checagem de tipos

    def exibir_feed(self):
        print("\n===== FEED FOCUS U =====")
        feed = self.postagens + self.eventos
        if not feed:
            print("Feed vazio.")
            return
        for item in feed:
            print(item.publicar())  # Chamada dinâmica polimórfica
            print("-" * 40)


    def estatisticas(self):
        print("\n===== ESTATÍSTICAS =====")
        print(f"Alunos Ativos: {UsuarioBase.total_usuarios}")
        print(f"Postagens Ativas: {Postagem.total_postagens}")
        print(f"Disciplinas no App: {Disciplina.total_disciplinas}")
        print(f"Rotinas Existentes: {Rotina.total_rotinas}")
