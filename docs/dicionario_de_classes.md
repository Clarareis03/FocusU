## 2. Dicionário de Classes

### Interfaces

| Classe | Tipo | Descrição | Membros principais |
|---|---|---|---|
| `Publicavel` | Interface (ABC) | Contrato obrigatório para qualquer entidade que possa ser exibida no feed. | `publicar()` (abstrato) |

### Classes abstratas

| Classe | Tipo | Descrição | Membros principais |
|---|---|---|---|
| `UsuarioBase` | Classe abstrata (ABC) | Modelo-base de herança para usuários do sistema. | `nome`, `email` (properties), `total_usuarios` (estático), `exibir_perfil()` (abstrato) |

### Entidades principais

| Classe | Herda/Implementa | Descrição | Atributos-chave | Métodos-chave |
|---|---|---|---|---|
| `Aluno` | `UsuarioBase` | Representa o estudante cadastrado no sistema, com login, disciplinas e rotinas. | `matricula`, `senha`, `foto_b64`, `disciplinas[]`, `rotinas[]` | `verificar_senha()`, `adicionar_disciplina()`, `adicionar_rotina()`, `calcular_tempo_estudo_recursivo()`, `obter_tarefas_pendentes()`, `obter_tarefas_atrasadas()`, `calcular_progresso_estudos()`, `atualizar_perfil()`, `to_dict()` / `from_dict()` |
| `Postagem` | `Publicavel` | Publicação genérica no feed acadêmico. | `titulo`, `conteudo`, `autor`, `curtidas`, `comentarios[]`, `total_postagens` (estático) | `curtir()`, `comentar()`, `publicar()` |
| `PostagemDuvida` | `Postagem` | Especialização para dúvidas de disciplina (polimorfismo). | `disciplina`, `resolvida` | `publicar()` sobrescrito |
| `PostagemMaterial` | `Postagem` | Especialização para compartilhamento de materiais (polimorfismo). | `link_download` | `publicar()` sobrescrito |
| `Evento` | `Publicavel` | Evento acadêmico institucional exibido no feed. | `titulo`, `data`, `horario`, `total_eventos` (estático) | `publicar()` |
| `Rotina` | — | Registro de tempo de estudo do aluno. | `atividade`, `tempo`, `total_rotinas` (estático) | Validação de `tempo > 0` via setter |
| `Disciplina` | — | Disciplina cadastrada no sistema, com tarefas e alunos matriculados. | `nome`, `professor`, `_tarefas{}`, `alunos_matriculados[]`, `total_disciplinas` (estático) | `adicionar_tarefa()`, `concluir_tarefa()`, `remover_tarefa()`, `listar_tarefas()` |
| `Tarefa` | — | Item de agenda de uma disciplina (prova, entrega, trabalho, lista). | `id`, `titulo`, `tipo`, `data_entrega`, `descricao`, `concluida`, `dono` | `marcar_concluida()`, `marcar_pendente()`, `esta_atrasada` (property) |

### Classe gerenciadora

| Classe | Descrição | Atributos-chave | Métodos-chave |
|---|---|---|---|
| `SistemaFocusU` | Centraliza o controle de alunos, disciplinas, postagens e eventos usando tabelas hash para busca O(1). | `alunos_por_matricula`, `alunos_por_email`, `disciplinas_por_nome`, `postagens[]`, `eventos[]` | `adicionar_aluno()`, `remover_aluno()` (com anonimização de posts), `adicionar_disciplina_global()`, `adicionar_postagem()`, `remover_postagem()`, `adicionar_evento()`, `redefinir_senha()`, `listar_alunos()`, `exibir_feed()`, `estatisticas()` |

### Hierarquia de exceções

Todas herdam de `FocusUError` (que herda de `Exception`):

| Exceção | Quando é lançada |
|---|---|
| `AlunoNaoEncontradoError` | Um aluno não é encontrado no sistema. |
| `DisciplinaNaoEncontradaError` | Uma disciplina não é encontrada no sistema. |
| `PostagemNaoEncontradaError` | Uma postagem não é encontrada. |
| `EventoNaoEncontradoError` | Um evento não é encontrado. |
| `MatriculaDuplicadaError` | Tentativa de cadastro com matrícula já existente. |
| `EmailDuplicadoError` | Tentativa de cadastro com e-mail já existente. |

---

### Pilares de POO representados

- **Abstração / Interfaces:** `Publicavel` (ABC) define o contrato `publicar()` implementado por `Postagem` e `Evento`.
- **Encapsulamento:** atributos protegidos (`_titulo`, `_nome`, `_email`, `_matricula`, `_tempo`, etc.) expostos via `@property` com validação nos setters.
- **Herança:** `Aluno` herda de `UsuarioBase`; `PostagemDuvida` e `PostagemMaterial` herdam de `Postagem`.
- **Polimorfismo:** cada subclasse de `Postagem` sobrescreve `publicar()` com formatação própria.
- **Gerenciamento de estado/memória:** uso de atributos estáticos (`total_alunos`, `total_postagens`, etc.) sincronizados via `__init__` / `__del__`.
