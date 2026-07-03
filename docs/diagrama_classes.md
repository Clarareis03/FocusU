# Diagrama de Classes UML - FocusU

Este diagrama representa a modelagem das classes, métodos, atributos e relacionamentos do sistema utilizando a sintaxe Mermaid.

```mermaid
classDiagram
class Publicavel {
  <<interface>>
  +publicar()
}

class UsuarioBase {
  <<abstract>>
  - _nome: str
  - _email: str
  + total_usuarios: int
  + __init__(nome, email)
  + __del__()
  + nome()
  + email()
  + exibir_perfil() *abstract*
}

class Aluno {
  + matricula: str
  + disciplinas: list
  + rotinas: list
  + adicionar_disciplina(disciplina)
  + adicionar_rotina(rotina)
  + exibir_perfil()
  + __str__()
}

class Postagem {
  + titulo: str
  + conteudo: str
  + autor: Aluno
  + curtidas: int
  + comentarios: list
  + total_postagens: int
  + __init__(titulo, conteudo, autor)
  + __del__()
  + curtir()
  + comentar(comentario)
  + publicar()
}

class PostagemDuvida {
  + disciplina: str
  + resolvida: bool
  + publicar()
}

class PostagemMaterial {
  + link_download: str
  + publicar()
}

class Evento {
  + titulo: str
  + data: str
  + horario: str
  + total_eventos: int
  + __init__(titulo, data, horario)
  + __del__()
  + publicar()
}

class Disciplina {
  - _nome: str
  + professor: str
  + total_disciplinas: int
  + __init__(nome, professor)
  + __del__()
  + nome()
  + __str__()
}

class Rotina {
  - _atividade: str
  - _tempo: int
  + total_rotinas: int
  + __init__(atividade, tempo)
  + __del__()
  + atividade()
  + tempo()
  + __str__()
}

class SistemaFocusU {
  + alunos: list
  + disciplinas_globais: list
  + postagens: list
  + eventos: list
  + adicionar_aluno(aluno)
  + remover_aluno(aluno)
  + adicionar_disciplina_global(d)
  + adicionar_postagem(p)
  + adicionar_evento(e)
  + listar_alunos()
  + exibir_feed()
  + estatisticas()
}

Aluno --|> UsuarioBase
Postagem ..|> Publicavel
Evento ..|> Publicavel
PostagemDuvida --|> Postagem
PostagemMaterial --|> Postagem
Disciplina o-- Aluno
Rotina *-- Aluno
Postagem --> Aluno : autor
SistemaFocusU o-- Aluno
SistemaFocusU o-- Disciplina
SistemaFocusU o-- Postagem
SistemaFocusU o-- Evento