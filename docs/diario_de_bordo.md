# 📓 Diário de Bordo — Projeto FocusU

> **Projeto:** FocusU — Plataforma de Organização Universitária
> **Documento:** Consolidação dos Diários de Bordo (Etapas de Recursão, Persistência, Estruturas de Dados e Interface Web)
> **Equipe:** Ayra · Clara Reis · Ana Beatriz

---

## 1. Visão Geral e Arquitetura do Projeto

O **FocusU** é uma aplicação em **Python 3.x**, originalmente concebida como uma ferramenta de linha de comando (CLI) e posteriormente evoluída para uma **aplicação web em Streamlit**, com o objetivo de auxiliar estudantes universitários na gestão de rotinas de estudo, disciplinas, tarefas (Agenda) e engajamento acadêmico (Feed social).

**Stack utilizada:**
- **Linguagem:** Python 3.x
- **Framework Web:** Streamlit
- **Visualização de Dados:** Pandas e Plotly (gráficos de distribuição de conteúdo no dashboard)
- **Manipulação de Imagem:** Pillow (fotos de perfil e de postagens em Base64)
- **Armazenamento Local:** arquivo `dados_focusu.json`
- **Controle de Versão / Hospedagem:** Git & GitHub, com deploy no Streamlit Community Cloud

**Padrão arquitetural:** o projeto manteve uma separação clara de camadas:
- **CLI (`main.py`):** interface original de terminal, preservada 100% intacta durante a migração para a Web.
- **Web (`src/web/`):** `interface_web.py` (roteador principal / menu lateral em sidebar) e `paginas.py` (renderização individual de cada tela).
- **Núcleo POO (`src/models/` / `src/system/`):** classes de domínio (`UsuarioBase`, `Aluno`, `Disciplina`, `Tarefa`, `Postagem`, `Evento`) e a classe gerenciadora `SistemaFocusU`, isoladas das camadas de apresentação.
- **Persistência (`src/utils/persistencia.py`):** camada dedicada de serialização/desserialização entre os objetos Python e o arquivo JSON.

Essa separação permitiu que as páginas web consumissem diretamente a instância global do `SistemaFocusU` (armazenada em `st.session_state`), reaproveitando integralmente as regras de negócio, contratos e validações já implementados no núcleo, sem duplicação de lógica.

---

## 2. Divisão de Responsabilidades e Contribuições

| Integrante | Área de Atuação | Principais Entregas |
|---|---|---|
| **Ayra** | Algoritmos e Núcleo POO | Implementação do algoritmo recursivo `calcular_tempo_estudo_recursivo()` na classe `Aluno`, tratamento defensivo de tipos e mensagens de erro amigáveis no `main.py`, nova opção de menu (Opção 13) na CLI. |
| **Clara Reis** | Interface Web (Streamlit) e Autenticação | Criação de `src/web/` (`interface_web.py` e `paginas.py`), Feed estilo Instagram com fotos/comentários/curtidas, Dashboard de KPIs, deploy no Streamlit Community Cloud, telas de **Entrar/Criar Conta** com upload de foto de perfil em Base64, ajuste de `requirements.txt`. |
| **Ana Beatriz** | Estruturas de Dados e Persistência | Refatoração de listas para dicionários (Tabela Hash O(1)), encapsulamento estrito da classe `Tarefa` via `@property`/`@setter`, criação e evolução do módulo `persistencia.py` (`sistema_para_dict()` / `dict_para_sistema()`), correções de roteamento e de integridade dos dados salvos. |

---

## 3. Evolução do Desenvolvimento (Linha do Tempo Funcional)

### Fase 1 — Núcleo POO, Algoritmos e Otimização O(1)

- **Classes de domínio:** `UsuarioBase` (classe abstrata, com `@abstractmethod exibir_perfil()`) e sua subclasse `Aluno`, além de `Disciplina`, `Tarefa`, `Postagem` e `Evento`, todas com encapsulamento via `@property`/`@setter`.
- **Recursão para métricas de estudo:** criação do método `calcular_tempo_estudo_recursivo()` em `models/usuario.py` (classe `Aluno`), somando o tempo das rotinas sem uso de `for`/`while` (soma do índice atual + chamada recursiva para `indice + 1` até o caso base). Complexidade **O(n)**, onde *n* é o número de rotinas do aluno. Mantido dentro da classe `Aluno` (e não em `SistemaFocusU`) por respeito ao encapsulamento, já que a lista de rotinas pertence à própria instância.
- **Otimização de buscas — Tabela Hash O(1):** substituição de listas simples por dicionários indexados: `alunos_por_matricula`, `alunos_por_email` (em caixa baixa) e `disciplinas_por_nome` (chave normalizada), eliminando buscas lineares O(n) na validação de duplicidade.
- **Normalização de chaves:** método `_normalizar_chave()` em `sistema.py`, usando a biblioteca nativa `unicodedata` para remover acentos, converter para minúsculas e aplicar `.strip()`, evitando duplicidade como "Análise de Dados" vs. "analise de dados".
- **Encapsulamento estrito da classe `Tarefa`:** propriedades privadas (`_concluida`, `_titulo`, etc.) expostas via `@property`, incluindo posteriormente o `@concluida.setter` para permitir a alternância booleana (`tarefa.concluida = False`) a partir da interface.
- **Robustez em memória:** correção do método `remover_aluno()` para excluir atomicamente o registro em **ambos** os dicionários (`alunos_por_matricula` e `alunos_por_email`), evitando inconsistência ao tentar recadastrar o mesmo e-mail.

### Fase 2 — Camada de Persistência JSON e Estado

- **Módulo `persistencia.py`** (posteriormente organizado em `src/utils/persistencia.py`): implementação das funções bidirecionais `sistema_para_dict()` (serialização) e `dict_para_sistema()` (desserialização), convertendo entre os objetos OO em memória e a estrutura plana do JSON.
- **Mapeamento de atributos complexos:** senhas, fotos de perfil e de postagens em Base64, rotinas individuais de estudo e autorias de postagens/comentários.
- **Integração com o estado da sessão:** uso de `st.session_state` para manter a instância do `SistemaFocusU` viva durante toda a navegação do usuário, sem necessidade de reprocessar o sistema a cada clique.
- **Confiabilidade no recarregamento:** reset explícito das estruturas em memória (`sistema.alunos_por_matricula = {}`, `sistema.disciplinas_por_nome = {}`, `sistema.postagens = []`, `sistema.eventos = []`) no início de `dict_para_sistema()`, evitando duplicação de registros a cada carregamento do JSON.
- **Estabilidade do arquivo físico:** definição do caminho absoluto de `dados_focusu.json` na raiz do projeto via `pathlib.Path` (`PROJECT_ROOT`), eliminando divergências entre execução local e nuvem, com rotina programática para zerar arquivo e dicionários em memória de forma atômica quando necessário.

### Fase 3 — Interface Web Responsiva & Feed Social (Streamlit)

- **Migração da CLI para a Web:** criação de `src/web/interface_web.py` (roteador principal / sidebar) e `paginas.py` (telas individuais), mantendo o `main.py` da CLI 100% intacto.
- **Feed Interativo Multimídia:** cards centralizados em modo escuro (Dark Mode), upload de fotos de capa/posts, filtro por tipo (Geral, Dúvidas, Materiais e Eventos), sistema de curtidas e caixa de comentários com seleção de autor via `st.selectbox`.
- **Dashboard de Estatísticas & KPIs:** painel com métricas gerais (alunos, posts, curtidas, comentários) e gráfico de distribuição de conteúdos via Pandas/Plotly.
- **Agenda de Tarefas:** telas de gerenciamento com filtro por status, apoiadas nos setters encapsulados da classe `Tarefa`.
- **Sistema de Autenticação e Perfil:** abas de **Entrar** e **Criar Conta**, formulário com validação de campos obrigatórios (nome, e-mail, matrícula e senha) e tratamento de imagem de perfil via upload/Base64.
- **Configuração e Deploy:** `requirements.txt` (`streamlit`, `pandas`, `Pillow`, `plotly`) e `README.md` atualizados com instruções de execução via Web.

---

## 4. Compêndio Técnico de Erros, Bugs e Soluções

### 4.1 Lógica de POO e Estruturas de Dados

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| `TypeError: Can't instantiate abstract class Aluno without an implementation for abstract method 'exibir_perfil'` | A classe mãe `UsuarioBase` define `@abstractmethod exibir_perfil()`; por inconsistência de nome ou célula não executada no Notebook, o Python entendeu que `Aluno` não cumpria o contrato. | Reimplementação garantida de `exibir_perfil()` em `Aluno` e reordenação da execução das células no Jupyter Notebook para atualizar a classe em memória. | Ayra |
| Duplicidade de disciplinas por variação de acentuação/maiúsculas (ex.: "Análise de Dados" e "analise de dados" tratados como registros distintos) | Comparação exata de caracteres na chave do dicionário, gerando hashes diferentes. | Criação de `_normalizar_chave()` em `sistema.py`, usando `unicodedata` para remover acentos + `.lower()` + `.strip()`. | Ana Beatriz |
| Inconsistência ao remover aluno: a chave de matrícula era excluída, mas a chave de e-mail permanecia cadastrada, bloqueando novo cadastro com o mesmo e-mail. | `remover_aluno()` não limpava as duas tabelas hash de forma atômica. | Atualização de `remover_aluno()` para excluir simultaneamente as chaves correspondentes em `alunos_por_matricula` e `alunos_por_email`. | Ana Beatriz |
| `AttributeError: property 'concluida' of 'Tarefa' object has no setter` ao desmarcar uma tarefa concluída. | `concluida` estava definido apenas com `@property` (somente leitura) na classe `Tarefa`. | Adição do `@concluida.setter` em `src/models/tarefa.py`, liberando `tarefa.concluida = False` com conversão garantida via `bool(valor)`. | Ana Beatriz |

### 4.2 Lógica Recursiva e Tratamento de Erros na CLI

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| Recursão de `calcular_tempo_estudo_recursivo()` quebrava (`TypeError`/`ValueError`) ao encontrar rotinas com tempo em texto (ex.: `"2h"`, `"30min"`). | Ausência de tipagem rígida/tratamento local; Python não soma `int` com `str`. | Programação defensiva com bloco `try/except` local dentro da própria função recursiva: se o tempo não puder ser convertido para `int`, exibe aviso, assume `0` para aquela rotina e **não interrompe** o cálculo das demais. | Ayra |
| Mensagens técnicas em inglês do próprio Python (`invalid literal for int() with base 10`) e falhas por entradas inválidas (`ValueError`/`IndexError`) derrubavam o menu da CLI. | O bloco `except ValueError as erro_val` repassava a string bruta do erro ao `print()`; ausência de pré-checagem para opções/índices inválidos. | Adição do conjunto `OPCOES_VALIDAS` para checagem O(1) no menu, blindagem global com `try/except` (`ValueError`/`IndexError`) e substituição das mensagens técnicas por avisos amigáveis em português (ex.: *"Por favor, digite apenas números inteiros sem letras"*) no `main.py`. | Ayra / Ana Beatriz |

### 4.3 Persistência / JSON

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| Ao encerrar e reabrir o sistema, o JSON não restaurava as disciplinas associadas ao perfil do aluno, a lista de alunos matriculados por disciplina, nem o "dono" original de cada tarefa. | `persistencia.py` omitia a lista `disciplinas` do dicionário de alunos, o atributo `alunos_matriculados` das disciplinas e a propriedade `dono` dos objetos `Tarefa`. | Reformulação de `sistema_para_dict()` e `dict_para_sistema()` para mapear a lista de nomes de disciplinas do aluno, a lista de matrículas vinculadas às cadeiras e a amarração bidirecional dos donos das tarefas. | Ana Beatriz |
| Duplicação/acúmulo de objetos em memória a cada recarregamento do JSON. | `dict_para_sistema()` não resetava as estruturas em memória antes de recriar os objetos a partir do arquivo. | Inclusão de reset explícito no início de `dict_para_sistema()`: `sistema.alunos_por_matricula = {}`, `sistema.disciplinas_por_nome = {}`, `sistema.postagens = []`, `sistema.eventos = []`. | Ana Beatriz |
| Dados antigos reapareciam mesmo após tentativas de exclusão/reinício do projeto ("persistência fantasma"); inconsistência de localização do arquivo entre ambiente local e nuvem. | `dados_focusu.json` permanecia salvo fisicamente na raiz do projeto e era lido automaticamente por `carregar_sistema_json()`, independentemente do ambiente de execução. | Mapeamento do caminho absoluto do banco local via `pathlib.Path` (`PROJECT_ROOT`), instruções de exclusão manual (`Remove-Item dados_focusu.json`) e criação de rotina programática para zerar arquivo e dicionários em memória atomicamente. | Ana Beatriz / Clara Reis |
| Falhas de login causadas por espaços adicionais nos campos e incompatibilidade com registros antigos salvos sem senha. | Ausência de padronização/normalização dos dados de formulário e de campo `senha` em cadastros legados. | Padronização com `.strip()` e conversão explícita para `str`, com gravação forçada imediatamente após o cadastro da senha. | Clara Reis |

### 4.4 Interface / Streamlit

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| Comentários do Feed exibidos em caixas brancas desconfiguradas (`st.expander`), com autor fixo como "Anônimo". | `.comentar("texto")` armazenava apenas uma string simples, sem registrar a entidade do aluno autor; limitação visual dos componentes nativos do Streamlit. | Reestruturação da área de comentários em HTML/CSS customizado (avatar + nome em negrito + texto), com `st.selectbox` para escolher o aluno comentando; comentário persistido no formato `Autor::Texto`. | Clara Reis |
| A Agenda foi implementada, mas não aparecia na navegação e não podia ser acessada. | `interface_web.py` não continha a importação de `tela_agenda`, o item correspondente em `menu_items` nem a condição de roteamento. | Importação da função, adição da tupla `("Agenda", "calendar_today")` no menu da sidebar e inclusão do bloco `elif pagina_atual == "Agenda": tela_agenda(sistema)`. | Ana Beatriz |
| Ao filtrar por "Concluídas" na Agenda, tarefas pendentes continuavam sendo renderizadas dentro do expander da disciplina. | Ausência de filtragem explícita na renderização dos cards e falta de atualização imediata do ciclo de vida do Streamlit ao alternar o checkbox. | Filtro de segurança via *list comprehension* diretamente em `tela_agenda` (`[t for t in tarefas if t.concluida]`) e chamada de `st.rerun()` logo após a alteração de status. | Ana Beatriz |

### 4.5 Deploy / Resolução de Caminhos e Módulos

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| `ModuleNotFoundError` na configuração inicial dos imports entre os pacotes internos do projeto. | Estrutura de pastas (`src/`, `src/web/`, `src/utils/`) ainda não padronizada. | Padronização das rotas de importação e ajuste na estrutura de pacotes internos em `src/`. | Clara Reis |
| Deploy no Streamlit Cloud falhava com `No module named 'plotly'`. | Bibliotecas de gráficos/imagem usadas no front-end não constavam no `requirements.txt` da raiz do repositório. | Atualização do `requirements.txt` incluindo `plotly`, `pandas`, `Pillow` e `streamlit` com versões mínimas compatíveis. | Clara Reis |
| `ModuleNotFoundError: No module named 'paginas'` ao rodar a partir de `src/web/interface_web.py` no servidor remoto. | Divergência entre o diretório de execução do Streamlit Cloud (raiz `/mount/src/focusu/`) e a estrutura interna de subpastas do repositório. | Ajuste dinâmico no topo de `interface_web.py` com `Path` e `sys.path.insert()`, adicionando explicitamente `PROJECT_ROOT`, `SRC_DIR` e `WEB_DIR` ao `sys.path`. | Clara Reis |

---

## 5. Ganhos de Desempenho e Resultados Alcançados

- **Complexidade de tempo:** redução de **O(n) → O(1)** nas verificações, buscas e exclusões de alunos (matrícula/e-mail) e disciplinas, via tabelas hash (`alunos_por_matricula`, `alunos_por_email`, `disciplinas_por_nome`).
- **Recursão controlada:** cálculo do tempo total de estudo em **O(n)** (onde *n* = número de rotinas), sem uso de laços tradicionais, tornado resiliente a dados corrompidos ou mal formatados no histórico do aluno.
- **Desacoplamento de camadas:** isolamento total entre a camada de apresentação (`src/web/`) e o núcleo de regras de negócio (`src/system/`, `src/models/`), respeitando os princípios de POO — a lógica recursiva, por exemplo, ficou 100% isolada na regra de negócio (`Aluno`), permitindo que a interface gráfica apenas a acione via botão, sem refatoração adicional.
- **Persistência entre sessões:** gravação e leitura em disco no formato JSON, preservando (segundo os diários) atributos essenciais como senhas, fotos, matrículas e autorias, com reset atômico das estruturas em memória a cada recarregamento.
- **Confiabilidade da interface:** roteamento reativo via `st.session_state`, com atualização instantânea de estado via `st.rerun()`.
- **Experiência do usuário (UX):** substituição de mensagens técnicas do interpretador Python por avisos amigáveis em português, layout customizado do Feed (estilo Instagram, Dark Mode) e dashboard analítico com KPIs e gráficos Plotly.
- **Acessibilidade:** transformação de uma aplicação estática de terminal em uma Web App responsiva, interativa e acessível via URL pública no navegador.
