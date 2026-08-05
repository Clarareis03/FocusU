# Diagrama de Classes — FocusU

Este documento reúne o diagrama UML (em Mermaid) e o dicionário de classes do sistema **FocusU**, cobrindo os pilares de POO aplicados no projeto: abstração/interfaces, encapsulamento, herança e polimorfismo.

## 1. Diagrama UML (Mermaid)

```mermaid
classDiagram
    direction TB

    class Publicavel {
        <<interface>>
        +publicar()* str
    }

    class UsuarioBase {
        <<abstract>>
        -_nome str
        -_email str
        +total_usuarios int$
        +nome str
        +email str
        +exibir_perfil()* str
    }

    class Aluno {
        -_senha str
        +matricula str
        +foto_b64 str
        +disciplinas list~Disciplina~
        +rotinas list~Rotina~
        +senha str
        +verificar_senha(senha_digitada) bool
        +adicionar_disciplina(disciplina)
        +adicionar_rotina(rotina)
        +exibir_perfil() str
        +calcular_tempo_estudo_recursivo(indice) int
        +obter_tarefas_pendentes(sistema) list
        +obter_tarefas_atrasadas(sistema) list
        +calcular_progresso_estudos(sistema) float
        +atualizar_perfil(...)
        +to_dict() dict
        +from_dict(dados)$ Aluno
    }

    class Postagem {
        -_titulo str
        -_conteudo str
        +autor Aluno
        +curtidas int
        +comentarios list
        +total_postagens int$
        +titulo str
        +conteudo str
        +curtir()
        +comentar(comentario)
        +publicar() str
    }

    class PostagemDuvida {
        +disciplina str
        +resolvida bool
        +publicar() str
    }

    class PostagemMaterial {
        +link_download str
        +publicar() str
    }

    class Evento {
        -_titulo str
        +data str
        +horario str
        +total_eventos int$
        +titulo str
        +publicar() str
    }

    class Rotina {
        -_atividade str
        -_tempo int
        +total_rotinas int$
        +atividade str
        +tempo int
    }

    class Disciplina {
        -_nome str
        +professor str
        -_tarefas dict~str, Tarefa~
        +total_disciplinas int$
        +alunos_matriculados list
        +nome str
        +adicionar_tarefa(...) Tarefa
        +concluir_tarefa(id_tarefa) bool
        +remover_tarefa(id_tarefa) bool
        +listar_tarefas(status) list~Tarefa~
    }

    class Tarefa {
        -_id str
        -_titulo str
        -_tipo str
        -_data_entrega date
        -_descricao str
        -_concluida bool
        +dono str
        +TIPOS_VALIDOS tuple$
        +id str
        +titulo str
        +tipo str
        +data_entrega date
        +descricao str
        +concluida bool
        +esta_atrasada bool
        +marcar_concluida()
        +marcar_pendente()
    }

    class SistemaFocusU {
        +alunos_por_matricula dict
        +alunos_por_email dict
        +disciplinas_por_nome dict
        +postagens list~Postagem~
        +eventos list~Evento~
        +adicionar_aluno(aluno)
        +remover_aluno(aluno)
        +adicionar_disciplina_global(d)
        +adicionar_postagem(p)
        +remover_postagem(postagem_alvo) bool
        +adicionar_evento(e)
        +redefinir_senha(email, matricula, nova_senha) bool
        +listar_alunos()
        +exibir_feed()
        +estatisticas()
    }

    class FocusUError {
        <<exception>>
    }
    class AlunoNaoEncontradoError
    class DisciplinaNaoEncontradaError
    class PostagemNaoEncontradaError
    class EventoNaoEncontradoError
    class MatriculaDuplicadaError
    class EmailDuplicadoError

    %% ===== HERANÇA / IMPLEMENTAÇÃO =====
    UsuarioBase <|-- Aluno
    Publicavel <|.. Postagem
    Publicavel <|.. Evento
    Postagem <|-- PostagemDuvida
    Postagem <|-- PostagemMaterial

    FocusUError <|-- AlunoNaoEncontradoError
    FocusUError <|-- DisciplinaNaoEncontradaError
    FocusUError <|-- PostagemNaoEncontradaError
    FocusUError <|-- EventoNaoEncontradoError
    FocusUError <|-- MatriculaDuplicadaError
    FocusUError <|-- EmailDuplicadoError

    %% ===== ASSOCIAÇÕES / COMPOSIÇÃO =====
    Aluno "1" o-- "0..*" Disciplina : disciplinas
    Aluno "1" *-- "0..*" Rotina : rotinas
    Disciplina "1" *-- "0..*" Tarefa : tarefas
    Postagem "0..*" --> "0..1" Aluno : autor

    SistemaFocusU "1" o-- "0..*" Aluno : alunos_por_matricula
    SistemaFocusU "1" o-- "0..*" Disciplina : disciplinas_por_nome
    SistemaFocusU "1" *-- "0..*" Postagem : postagens
    SistemaFocusU "1" *-- "0..*" Evento : eventos