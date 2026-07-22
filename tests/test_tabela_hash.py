import os
import sys
import pytest

# Garante que o Python encontre as pastas 'models' e 'system' independente de onde o pytest for chamado
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_ATUAL, ".."))
PASTA_SRC = os.path.abspath(os.path.join(DIRETORIO_ATUAL, "../src"))

sys.path.insert(0, RAIZ_PROJETO)
sys.path.insert(0, PASTA_SRC)

from models.usuario import Aluno
from models.disciplina import Disciplina
from system.sistema import SistemaFocusU


def test_cadastro_aluno_sucesso():
    sistema = SistemaFocusU()
    aluno = Aluno("Ayra", "ayra@email.com", "100")
    sistema.adicionar_aluno(aluno)
    assert "100" in sistema.alunos_por_matricula
    assert "ayra@email.com" in sistema.alunos_por_email


def test_bloqueio_matricula_duplicada():
    sistema = SistemaFocusU()
    aluno1 = Aluno("Ayra", "ayra@email.com", "100")
    aluno2 = Aluno("Beatriz", "beatriz@email.com", "100")
    sistema.adicionar_aluno(aluno1)

    with pytest.raises(ValueError, match="já está cadastrada"):
        sistema.adicionar_aluno(aluno2)


def test_bloqueio_email_duplicado():
    sistema = SistemaFocusU()
    aluno1 = Aluno("Ayra", "ayra@email.com", "100")
    aluno2 = Aluno("Clara", "AYRA@email.com", "200")
    sistema.adicionar_aluno(aluno1)

    with pytest.raises(ValueError, match="já está em uso"):
        sistema.adicionar_aluno(aluno2)


def test_bloqueio_disciplina_duplicada_normalizada():
    sistema = SistemaFocusU()
    d1 = Disciplina("Análise de Dados", "Prof. Carlos")
    d2 = Disciplina("analise de dados", "Prof. Ana")
    sistema.adicionar_disciplina_global(d1)

    with pytest.raises(ValueError, match="já existe no sistema"):
        sistema.adicionar_disciplina_global(d2)