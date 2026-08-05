# 📓 Diário de Bordo — Projeto FocusU

> **Projeto:** FocusU — Plataforma de Organização Universitária
> **Documento:** Consolidação dos Diários de Bordo (Etapas de Recursão, Persistência, Estruturas de Dados, Interface Web e Autonomia do Usuário)
> **Equipe:** Ayra · Clara Reis · Ana Beatriz

---

## 1. Visão Geral e Arquitetura do Projeto

O **FocusU** é uma aplicação em **Python 3.x**, originalmente concebida como uma ferramenta de linha de comando (CLI) e posteriormente evoluída para uma **aplicação web em Streamlit**, com o objetivo de auxiliar estudantes universitários na gestão de rotinas de estudo, disciplinas, tarefas privadas (Agenda) e engajamento acadêmico (Feed social).

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
- **Núcleo POO (`src/models/` / `src/system/`):** classes de domínio (`UsuarioBase`, `Aluno`, `Disciplina`, `Tarefa`, `Postagem`, `Evento`, `Rotina`) e a classe gerenciadora `SistemaFocusU`, isoladas das camadas de apresentação.
- **Persistência (`src/utils/persistencia.py`):** camada dedicada de serialização/desserialização entre os objetos Python e o arquivo JSON.

Essa separação permitiu que as páginas web consumissem diretamente a instância global do `SistemaFocusU` (armazenada em `st.session_state`), reaproveitando integralmente as regras de negócio, contratos, privacidade e validações já implementados no núcleo, sem duplicação de lógica.

---

## 2. Divisão de Responsabilidades e Contribuições

| Integrante | Área de Atuação | Principais Entregas |
|---|---|---|
| **Ayra** | Algoritmos e Núcleo POO | Implementação do algoritmo recursivo `calcular_tempo_estudo_recursivo()` na classe `Aluno`, tratamento defensivo de tipos e mensagens de erro amigáveis no `main.py`, nova opção de menu (Opção 13) na CLI. |
| **Clara Reis** | Interface Web (Streamlit) e Autenticação | Criação de `src/web/` (`interface_web.py` e `paginas.py`), Feed estilo Instagram com fotos/comentários/curtidas, Dashboard de KPIs, deploy no Streamlit Community Cloud, telas de **Entrar/Criar Conta** com upload de foto de perfil em Base64, ajuste de `requirements.txt`. |
| **Ana Beatriz** | Estruturas de Dados, Persistência e Autonomia | Refatoração de listas para dicionários (Tabela Hash O(1)), encapsulamento da classe `Tarefa`, integração do modelo `Rotina` para tempo de estudo, módulos de privacidade na Agenda, fluxo de redefinição de senha, cancelamento de matrícula e apagar posts, criação e evolução do módulo `persistencia.py`. |

---

## 3. Evolução do Desenvolvimento (Linha do Tempo Funcional)

### Fase 1 — Núcleo POO, Algoritmos e Otimização O(1)

- **Classes de domínio:** `UsuarioBase` (classe abstrata, com `@abstractmethod exibir_perfil()`) e sua subclasse `Aluno`, além de `Disciplina`, `Tarefa`, `Postagem`, `Evento` e `Rotina`, todas com encapsulamento via `@property`/`@setter`.
- **Integração do Modelo `Rotina`:** conexão do modelo de rotinas de estudo diretamente ao perfil do aluno. O preenchimento manual ou a conclusão de uma tarefa gera uma nova instância de `Rotina` associada, acumulando o tempo total de dedicação acadêmica.
- **Recursão para métricas de estudo:** criação do método `calcular_tempo_estudo_recursivo()` em `models/usuario.py` (classe `Aluno`), somando o tempo das rotinas sem uso de `for`/`while` (soma do índice atual + chamada recursiva para `indice + 1` até o caso base). Complexidade **O(n)**, onde *n* é o número de rotinas do aluno. Mantido dentro da classe `Aluno` por respeito ao encapsulamento.
- **Otimização de buscas — Tabela Hash O(1):** substituição de listas simples por dicionários indexados: `alunos_por_matricula`, `alunos_por_email` (em caixa baixa) e `disciplinas_por_nome` (chave normalizada), eliminando buscas lineares O(n) na validação de duplicidade.
- **Normalização de chaves:** método `_normalizar_chave()` em `sistema.py`, usando `unicodedata` para remover acentos, converter para minúsculas e aplicar `.strip()`, evitando duplicidades como "Análise de Dados" vs. "analise de dados".
- **Encapsulamento estrito da classe `Tarefa`:** propriedades privadas (`_concluida`, `_titulo`, etc.) expostas via `@property`, incluindo o `@concluida.setter` para permitir a alternância booleana (`tarefa.concluida = False`) a partir da interface.
- **Robustez em memória:** correção do método `remover_aluno()` para excluir atomicamente o registro em **ambos** os dicionários (`alunos_por_matricula` e `alunos_por_email`).

### Fase 2 — Camada de Persistência JSON e Estado

- **Módulo `persistencia.py` (`src/utils/persistencia.py`):** implementação das funções bidirecionais `sistema_para_dict()` (serialização) e `dict_para_sistema()` (desserialização) para conversão entre os objetos OO em memória e a estrutura do JSON.
- **Mapeamento de atributos complexos:** preservação de senhas salvas, fotos em Base64, histórico de rotinas individuais de estudo, atribuição bidirecional do dono original de tarefas/postagens, comentários e lista de alunos matriculados por disciplina.
- **Integração com o estado da sessão:** uso de `st.session_state` para manter a instância do `SistemaFocusU` viva durante a navegação, sem necessidade de reprocessar o sistema a cada clique.
- **Confiabilidade no recarregamento:** reset explícito das estruturas em memória no início de `dict_para_sistema()`, evitando duplicação de registros a cada leitura do arquivo JSON.
- **Estabilidade do arquivo físico:** definição do caminho absoluto de `dados_focusu.json` na raiz do projeto via `pathlib.Path` (`PROJECT_ROOT`), eliminando divergências entre execução local e nuvem.

### Fase 3 — Interface Web Responsiva, Privacidade & Autonomia do Aluno (Streamlit)

- **Migração da CLI para a Web:** criação de `src/web/interface_web.py` (roteador principal / sidebar) e `paginas.py` (telas individuais), mantendo o `main.py` da CLI intacto.
- **Feed Interativo Multimídia & Gestão de Conteúdo:** cards centralizados em Dark Mode, upload de fotos, filtro por tipo, curtidas, comentários (`Autor::Texto`) e verificação de autoridade que exibe o botão **"Apagar Postagem"** exclusivamente para o criador do post.
- **Dashboard de Estatísticas & KPIs:** painel com métricas gerais e gráfico de distribuição de conteúdos via Pandas/Plotly.
- **Agenda Privada & Rastreio de Estudos:** 
  - *Filtro estrito de privacidade:* exibição de tarefas restrita unicamente ao aluno autor (`dono == aluno_logado.matricula`).
  - *Integração com Tempo de Estudo:* substituição do botão simples de conclusão por uma interface composta (input numérico + botão). Ao concluir a tarefa, o tempo digitado é registrado automaticamente como uma nova `Rotina` no perfil do aluno.
- **Autonomia de Perfil & Autenticação:**
  - *Gestão de Matrículas:* seção "Minhas Matrículas Ativas" com botões dinâmicos para desmatricular-se de disciplinas.
  - *Recuperação de Acesso:* aba **"Esqueci a Senha"** na área de login, permitindo a sobrescrita segura da senha via validação cruzada de e-mail e matrícula.
- **Configuração e Deploy:** `requirements.txt` e `README.md` atualizados para execução e hospedagem contínua.

---

## 4. Compêndio Técnico de Erros, Bugs e Soluções

### 4.1 Lógica de POO e Estruturas de Dados

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| `TypeError: Can't instantiate abstract class Aluno without an implementation for abstract method 'exibir_perfil'` | A classe mãe `UsuarioBase` define `@abstractmethod exibir_perfil()`; por inconsistência de nome, o Python entendeu que `Aluno` não cumpria o contrato. | Reimplementação garantida de `exibir_perfil()` em `Aluno` e reordenação da execução no ambiente de desenvolvimento. | Ayra |
| Duplicidade de disciplinas por variação de acentuação/maiúsculas ("Análise de Dados" vs "analise de dados"). | Comparação exata de caracteres na chave do dicionário, gerando hashes diferentes. | Criação de `_normalizar_chave()` em `sistema.py`, usando `unicodedata` para remover acentos + `.lower()` + `.strip()`. | Ana Beatriz |
| Inconsistência ao remover aluno: chave de matrícula era excluída, mas chave de e-mail permanecia cadastrada. | `remover_aluno()` não limpava as duas tabelas hash de forma atômica. | Atualização de `remover_aluno()` para excluir simultaneamente as chaves em `alunos_por_matricula` e `alunos_por_email`. | Ana Beatriz |
| `AttributeError: property 'concluida' of 'Tarefa' object has no setter` ao desmarcar tarefa concluída. | `concluida` estava definido apenas com `@property` (somente leitura) na classe `Tarefa`. | Adição do decorator `@concluida.setter` em `src/models/tarefa.py`, liberando `tarefa.concluida = False` com conversão para `bool`. | Ana Beatriz |

### 4.2 Lógica Recursiva e Tratamento de Erros na CLI

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| Recursão de `calcular_tempo_estudo_recursivo()` quebrava ao encontrar rotinas com tempo em texto (ex.: `"2h"`, `"30min"`). | Ausência de tipagem rígida local; Python não soma `int` com `str`. | Programação defensiva com bloco `try/except` local na função recursiva: se a conversão falhar, exibe aviso, assume `0` e prossegue com as demais rotinas. | Ayra |
| Mensagens técnicas em inglês do Python e falhas por entradas inválidas derrubavam o menu da CLI. | Repasse da string bruta do erro ao `print()`; falta de pré-checagem para opções do menu. | Adição do conjunto `OPCOES_VALIDAS` para checagem O(1), blindagem global com `try/except` e mensagens amigáveis em português no `main.py`. | Ayra / Ana Beatriz |

### 4.3 Persistência / JSON

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| JSON não restaurava disciplinas do aluno, alunos matriculados na disciplina, nem o "dono" original da tarefa. | `persistencia.py` omitia a lista `disciplinas` do aluno, `alunos_matriculados` das disciplinas e a propriedade `dono` das tarefas. | Reformulação de `sistema_para_dict()` e `dict_para_sistema()` para mapear nomes de disciplinas, matrículas vinculadas e amarração bidirecional do dono da tarefa. | Ana Beatriz |
| Duplicação/acúmulo de objetos em memória a cada recarregamento do JSON. | `dict_para_sistema()` não resetava as estruturas em memória antes de recriar os objetos a partir do arquivo. | Inclusão de reset explícito no início de `dict_para_sistema()` (`alunos_por_matricula = {}`, `disciplinas_por_nome = {}`, `postagens = []`, `eventos = []`). | Ana Beatriz |
| Dados antigos reapareciam após exclusão/reinício ("persistência fantasma"). | `dados_focusu.json` permanecia na raiz e era lido automaticamente por `carregar_sistema_json()`. | Mapeamento do caminho absoluto via `pathlib.Path` (`PROJECT_ROOT`) e criação de rotina programática para zerar arquivo e memória de forma atômica. | Ana Beatriz / Clara Reis |
| Falhas de login causadas por espaços adicionais e registros antigos sem senha. | Ausência de padronização dos dados de formulário e de campo `senha` em cadastros legados. | Padronização com `.strip()`, conversão explícita para `str` e gravação forçada pós-cadastro. | Clara Reis |

### 4.4 Interface / Streamlit, Privacidade e Autonomia

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| Comentários do Feed em caixas brancas desconfiguradas e autor fixo como "Anônimo". | `.comentar("texto")` armazenava apenas string simples sem entidade do autor. | Reestruturação em HTML/CSS customizado (avatar + nome + texto) com `st.selectbox` de autor, persistido no formato `Autor::Texto`. | Clara Reis |
| Agenda não aparecia na barra de navegação gráfica. | `interface_web.py` não continha a importação da `tela_agenda` nem o roteamento correspondente. | Importação da função, inclusão do item na sidebar e adição do bloco condicional de navegação. | Ana Beatriz |
| Filtro de "Concluídas" na Agenda mantinha tarefas pendentes visíveis. | Ausência de filtragem explícita na renderização e falta de atualização imediata do ciclo do Streamlit. | Filtro de segurança por *list comprehension* (`[t for t in tarefas if t.concluida]`) e inserção do comando `st.rerun()`. | Ana Beatriz |
| Vazamento de tarefas entre usuários na Agenda (falta de privacidade). | Tela da Agenda exibia todas as tarefas criadas em uma disciplina para todos os alunos matriculados nela. | Implementação de filtro rigoroso no laço da `tela_agenda`, renderizando tarefas apenas se `dono == aluno_logado.matricula`. | Ana Beatriz |
| Tarefas concluídas não contabilizavam tempo no perfil do aluno. | O botão de conclusão apenas alterava o status booleano da tarefa sem capturar horas dedicadas. | Interface composta (input numérico + botão) que captura o tempo digitado e gera automaticamente uma nova `Rotina` vinculada ao perfil do aluno. | Ana Beatriz |
| Alunos presos a disciplinas erradas e impossibilidade de apagar posts próprios no Feed. | Ausência de botões para desmatricular e de verificação de autoria nos cards de postagens. | Adição da seção "Minhas Matrículas Ativas" com remoção dinâmica e verificação de autoridade no Feed exibindo "Apagar Postagem" apenas ao criador. | Ana Beatriz |
| Usuários bloqueados permanentemente ao esquecer a senha. | Interface não possuía fluxo de redefinição de credenciais de acesso. | Implementação da aba "Esqueci a Senha" no Login, validando dados cruzados (e-mail e matrícula) para redefinição segura da senha. | Ana Beatriz |

### 4.5 Deploy / Resolução de Caminhos e Módulos

| Problema | Causa Raiz | Solução Aplicada | Origem |
|---|---|---|---|
| `ModuleNotFoundError` na configuração de imports entre pacotes internos. | Estrutura de pastas ainda não padronizada. | Padronização das rotas de importação e ajuste na estrutura de pacotes em `src/`. | Clara Reis |
| Deploy no Streamlit Cloud falhava com `No module named 'plotly'`. | Bibliotecas do front-end omitidas no `requirements.txt`. | Atualização do `requirements.txt` com `plotly`, `pandas`, `Pillow` e `streamlit`. | Clara Reis |
| `ModuleNotFoundError: No module named 'paginas'` ao rodar na nuvem. | Divergência entre diretório de execução no servidor remoto e subpastas do repositório. | Ajuste dinâmico no topo de `interface_web.py` com `Path` e `sys.path.insert()`, incluindo `PROJECT_ROOT`, `SRC_DIR` e `WEB_DIR`. | Clara Reis |

---

## 5. Ganhos de Desempenho e Resultados Alcançados

- **Complexidade de tempo:** redução de **O(n) → O(1)** nas verificações, buscas e exclusões de alunos e disciplinas via tabelas hash (`alunos_por_matricula`, `alunos_por_email`, `disciplinas_por_nome`).
- **Recursão controlada & Rastreio de Estudo:** cálculo recursivo de tempo total de estudo em **O(n)** e integração contínua com a classe `Rotina`, convertendo tarefas concluídas na Agenda em histórico acumulado de horas de estudo.
- **Privacidade e Segurança dos Dados:** garantia de sigilo na Agenda de Tarefas (exibição estrita por aluno dono) e validação cruzada para recuperação de acesso na aba "Esqueci a Senha".
- **Autonomia do Usuário:** liberdade para o aluno gerenciar seu próprio perfil (cancelamento de matrículas ativas em "Minhas Matrículas Ativas" e exclusão de publicações de sua autoria no Feed).
- **Desacoplamento de camadas:** isolamento completo entre apresentação (`src/web/`) e regras de negócio (`src/system/`, `src/models/`), respeitando rigorosamente os princípios de POO.
- **Persistência Confiável:** gravação e leitura em disco no formato JSON mantendo integridade estrutural entre sessões (senhas, fotos, autorias, rotinas e matrículas), com reset atômico em memória.
- **Experiência do Usuário (UX) & Retenção:** navegação reativa via `st.session_state` e `st.rerun()`, layout moderno em Dark Mode, avisos amigáveis em português e dashboards analíticos com gráficos Plotly.