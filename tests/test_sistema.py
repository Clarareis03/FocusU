import sys
import os

# Adiciona a pasta raiz (FocusU) e a pasta src ao caminho de busca do Python
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(raiz, 'src')

if raiz not in sys.path:
    sys.path.insert(0, raiz)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import unittest
from src.models.usuario import Aluno, UsuarioBase
from src.models.disciplina import Disciplina
from src.models.rotina import Rotina
from src.models.postagem import Postagem, PostagemDuvida
from src.system.sistema import SistemaFocusU

class TestFocusU(unittest.TestCase):

    def setUp(self):
        """Executado antes de cada teste para resetar o estado do sistema."""
        self.sistema = SistemaFocusU()
        # Reseta os contadores estáticos para evitar interferência entre testes
        UsuarioBase.total_usuarios = 0
        Postagem.total_postagens = 0
        Disciplina.total_disciplinas = 0
        Rotina.total_rotinas = 0

    def test_cadastro_aluno_sucesso(self):
        """Testa se um aluno é cadastrado corretamente com dados válidos."""
        aluno = Aluno("Ayra", "ayra@email.com", "202601")
        self.assertEqual(aluno.nome, "Ayra")
        self.assertEqual(aluno.email, "ayra@email.com")
        self.assertEqual(aluno.matricula, "202601")

    ''' def test_validacao_nome_vazio(self):
        """Garante que o sistema lança ValueError se o nome for vazio."""
        with self.assertRaises(ValueError):
            aluno = Aluno("  ", "beatriz@email.com", "202602") '''

    ''' def test_validacao_email_invalido(self):
        """Garante que o sistema lança ValueError se o e-mail não contiver '@'."""
        with self.assertRaises(ValueError):
            aluno = Aluno("Clara", "clara_email.com", "202603")'''

    def test_validacao_tempo_rotina_negativo(self):
        """Garante que o tempo da rotina deve ser maior que zero."""
        with self.assertRaises(ValueError):
            Rotina("Estudar POO", 0)
        with self.assertRaises(ValueError):
            Rotina("Exercícios", -10)

    def test_remover_aluno_e_anonimizar_postagem(self):
        """Testa a exclusão segura: remoção do aluno e anonimização de seus posts."""
        aluno = Aluno("Bia", "bia@email.com", "202604")
        self.sistema.adicionar_aluno(aluno)
        
        post = Postagem("Dúvida Crucial", "O que é polimorfismo?", aluno)
        self.sistema.adicionar_postagem(post)

        # Remove o aluno do sistema
        self.sistema.remover_aluno(aluno)

        # O aluno não deve estar mais na lista do sistema
        self.assertNotIn(aluno, self.sistema.alunos)
        # A postagem continua existindo, mas o autor agora deve ser None (Usuário Anônimo)
        self.assertIsNone(post.autor)

    def test_contadores_estaticos_ciclo_de_vida(self):
        """Testa se os destrutores (__del__) atualizam corretamente os contadores globais."""
        aluno1 = Aluno("Ayra", "ayra@email.com", "202601")
        aluno2 = Aluno("Clara", "clara@email.com", "202603")
        self.assertEqual(UsuarioBase.total_usuarios, 2)

        # Força a destruição de um objeto para simular a limpeza de cache
        aluno2.__del__()
        self.assertEqual(UsuarioBase.total_usuarios, 1)

    def test_polimorfismo_publicacao(self):
        """Garante que as subclasses de Postagem formatam a publicação de maneiras diferentes."""
        aluno = Aluno("Ayra", "ayra@email.com", "202601")
        post_geral = Postagem("Aviso", "Aula amanhã", aluno)
        post_duvida = PostagemDuvida("Ajuda", "Erro no código", aluno, "POO II")

        self.assertIn("[POST GERAL]", post_geral.publicar())
        self.assertIn("[DÚVIDA - POO II]", post_duvida.publicar())

if __name__ == "__main__":
    unittest.main()