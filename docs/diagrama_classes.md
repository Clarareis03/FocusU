# 📐 Diagrama de Classes — FocusU

> Representação UML da arquitetura Orientada a Objetos do projeto FocusU, destacando herança, abstração (interfaces), encapsulamento e associações.

```mermaid
classDiagram
    %% ---------------------------------------------------------
    %% INTERFACES / ABSTRAÇÕES
    %% ---------------------------------------------------------
    class Publicavel {
        <<interface>>
        +exibir_detalhes()* String
    }

    %% ---------------------------------------------------------
    %% MODELOS PRINCIPAIS
    %% ---------------------------------------------------------
    class Usuario {
        <<abstract>>
        #_nome: String
        #_email: String
        #_matricula: String
        #_foto_b64: String
        +nome: String
        +email: String
        +matricula: String
        +foto_b64: String
        +validar_email(email) Static
    }

    class Aluno {
        -_disciplinas_matriculadas: List~Disciplina~
        -_rotina: Rotina
        +adicionar_disciplina(disciplina)
        +remover_disciplina(disciplina)
    }

    class Disciplina {
        -_nome: String
        -_codigo: String
        -_professor: String
        -_tarefas: List~Tarefa~
        +adicionar_tarefa(tarefa)
    }

    class Tarefa {
        -_titulo: String
        -_data_entrega: String
        -_concluida: bool
        +marcar_concluida()
    }

    class Rotina {
        -_horarios: List~String~
        +adicionar_horario(horario)
    }

    %% ---------------------------------------------------------
    %% POSTAGENS & EVENTOS (POLIMORFISMO & HERANÇA)
    %% ---------------------------------------------------------
    class Postagem {
        #_titulo: String
        #_conteudo: String
        #_autor: Usuario
        #_curtidas: int
        #_curtidores: Set~String~
        #_comentarios: List~String~
        #_foto_post_b64: String
        +curtir(user_id)
        +comentar(texto)
        +exibir_detalhes() String
    }

    class PostagemDuvida {
        -_disciplina: String
        -_resolvida: bool
        +marcar_resolvida()
        +exibir_detalhes() String
    }

    class PostagemMaterial {
        -_link_download: String
        +exibir_detalhes() String
    }

    class Evento {
        -_titulo: String
        -_data: String
        -_horario: String
        +exibir_detalhes() String
    }

    %% ---------------------------------------------------------
    %% GERENCIADOR CENTRAL DO SISTEMA
    %% ---------------------------------------------------------
    class SistemaFocusU {
        -_alunos: List~Aluno~
        -_disciplinas: List~Disciplina~
        -_postagens: List~Postagem~
        -_eventos: List~Evento~
        +cadastrar_aluno(aluno)
        +remover_aluno(matricula)
        +adicionar_postagem(postagem)
        +adicionar_evento(evento)
        +obter_estatisticas() Dict
    }

    %% ---------------------------------------------------------
    %% RELACIONAMENTOS (HERANÇA, IMPLEMENTAÇÃO & COMPOSIÇÃO)
    %% ---------------------------------------------------------
    Publicavel <|.. Postagem : Implementa
    Publicavel <|.. Evento : Implementa

    Usuario <|-- Aluno : Herança

    Postagem <|-- PostagemDuvida : Herança
    Postagem <|-- PostagemMaterial : Herança

    Aluno "1" *-- "1" Rotina : Composição
    Aluno "1" o-- "*" Disciplina : Agregação
    Disciplina "1" *-- "*" Tarefa : Composição
    Postagem "1" --> "1" Usuario : Associação (Autor)

    SistemaFocusU "1" o-- "*" Aluno : Gerencia
    SistemaFocusU "1" o-- "*" Disciplina : Gerencia
    SistemaFocusU "1" o-- "*" Postagem : Gerencia
    SistemaFocusU "1" o-- "*" Evento : Gerencia