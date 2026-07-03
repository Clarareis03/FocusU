class FocusUError(Exception):
    """Classe base para exceções do sistema FocusU."""
    pass


class AlunoNaoEncontradoError(FocusUError):
    """Lançada quando um aluno não é encontrado."""
    pass


class DisciplinaNaoEncontradaError(FocusUError):
    """Lançada quando uma disciplina não é encontrada."""
    pass


class PostagemNaoEncontradaError(FocusUError):
    """Lançada quando uma postagem não é encontrada."""
    pass


class EventoNaoEncontradoError(FocusUError):
    """Lançada quando um evento não é encontrado."""
    pass


class MatriculaDuplicadaError(FocusUError):
    """Lançada quando a matrícula já está cadastrada."""
    pass


class EmailDuplicadoError(FocusUError):
    """Lançada quando o e-mail já está cadastrado."""
    pass