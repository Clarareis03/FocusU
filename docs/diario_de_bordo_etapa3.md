## Refatoração de Estruturas de Dados, Persistência JSON e Interface Web

**Responsável:** Ana Beatriz  
**Data de Conclusão:** 24/07/2026 *(Atualizado com módulo de persistência local)*  

---

### 1. Mapeamento de Gargalos e Objetivos
- Foi mapeada a presença de buscas lineares $O(n)$ nas rotinas de validação de duplicidade de alunos (matrícula e e-mail) e disciplinas. Em cenários com muitos registros, o tempo de checagem crescia de forma proporcional ao número de elementos cadastrados.
- Houve a necessidade de integrar a lógica Orientada a Objetos (OO) do back-end com uma interface gráfica em **Streamlit**, criando telas para o gerenciamento de alunos, disciplinas e a **Agenda de Tarefas**.
- **Mecanismo de Persistência de Dados:** Implementação e aprimoramento de um sistema de salvamento/carregamento local via arquivo JSON (`dados_focusu.json`) para garantir a permanência de cadastros, postagens, eventos e tarefas entre reinicializações do servidor Web.

---

### 2. Alterações de Estrutura e Orientação a Objetos
- **Dicionários (Tabela Hash $O(1)$):** As listas simples foram substituídas por dicionários (`dict`), utilizando chaves únicas para buscas diretas:
  - `alunos_por_matricula`: Indexado pela matrícula do aluno.
  - `alunos_por_email`: Indexado pelo e-mail do aluno (em caixa baixa).
  - `disciplinas_por_nome`: Indexado pelo nome normalizado da disciplina.
- **Encapsulamento na Classe `Tarefa`:** Utilização de propriedades privadas (`_concluida`, `_titulo`, etc.) expostas via `@property` e `@setter` para garantir consistência de dados e controle de mutação na interface.
- **Camada de Persistência em JSON (`src/utils/persistencia.py`):**
  - Implementação das funções `sistema_para_dict()` (serialização) e `dict_para_sistema()` (desserialização) para conversão bidirecional entre os objetos OO do Python e a estrutura JSON.
  - Mapeamento e preservação de atributos complexos como: senhas salvas, fotos em Base64, rotinas individuais de estudos, autorias de postagens/comentários e lista de alunos matriculados por disciplina.

---

### 3. Erros Encontrados e Soluções

Durante o desenvolvimento, execução dos testes, integração com o Streamlit e refatoração da persistência de dados, surgiram os seguintes problemas e soluções:

#### 🐛 Bug 1: Duplicidade por Variação de Acentuação e Maiúsculas
- **Problema:** O sistema permitia cadastrar "Análise de Dados" e "analise de dados" como duas disciplinas distintas, pois as strings geravam hashes diferentes.
- **Causa:** Comparação exata de caracteres na chave do dicionário.
- **Solução:** Implementação do método `_normalizar_chave()` no `sistema.py` usando a biblioteca nativa `unicodedata` para remover acentos, converter o texto para minúsculas e aplicar `.strip()`.

#### 🐛 Bug 2: Entradas Inválidas Derrubando o Menu Terminal (`main.py`)
- **Problema:** Ao digitar letras onde se esperava números de opção ou ao selecionar índices inexistentes na lista, o Python disparava `ValueError` ou `IndexError` e encerrava a execução do programa.
- **Solução:** Adicionado um conjunto `OPCOES_VALIDAS` para pré-checagem em $O(1)$ no menu e blindagem global com bloco `try/except` capturando `ValueError` e `IndexError` graciosamente.

#### 🐛 Bug 3: Inconsistência ao Remover Aluno de Múltiplas Chaves
- **Problema:** Ao apagar uma conta de aluno, a chave da matrícula era removida do dicionário, mas a chave de e-mail permanecia cadastrada, impedindo novo cadastro com aquele e-mail.
- **Solução:** Atualização do método `remover_aluno()` para limpar atomicamente a chave correspondente em ambos os dicionários (`alunos_por_matricula` e `alunos_por_email`).

#### 🐛 Bug 4: Omissão da Agenda no Roteamento do Menu Lateral (`interface_web.py`)
- **Problema:** A funcionalidade de Agenda foi criada, mas não aparecia na barra de navegação gráfica e não podia ser acessada.
- **Causa:** O arquivo `interface_web.py` não continha a importação de `tela_agenda`, o item no array de navegação `menu_items` e a condição no bloco `if/elif` de roteamento de páginas.
- **Solução:** Atualização do `interface_web.py` com a importação da função, adição da tupla `("Agenda", "calendar_today")` no menu da sidebar e inclusão do bloco `elif pagina_atual == "Agenda": tela_agenda(sistema)`.

#### 🐛 Bug 5: Violabilidade/Falta de Setter no Encapsulamento (`AttributeError`)
- **Problema:** Ao desmarcar a caixinha de uma tarefa concluída na interface, a aplicação encerrava com `AttributeError: property 'concluida' of 'Tarefa' object has no setter`.
- **Causa:** O atributo `concluida` da classe `Tarefa` estava configurado apenas com o decorator `@property` (somente leitura), impedindo reatribuições diretas como `tarefa.concluida = False`.
- **Solução:** Adição do decorator `@concluida.setter` na classe `Tarefa` (`src/models/tarefa.py`), liberando a mutação do booleano com tipo garantido via `bool(valor)`.

#### 🐛 Bug 6: Ineficiência de Filtragem Dinâmica por Status na Interface Web
- **Problema:** Ao selecionar o filtro "Concluídas" nos radio buttons da Agenda, tarefas pendentes continuavam sendo renderizadas dentro do expander da disciplina.
- **Causa:** Ausência de uma filtragem explícita na renderização dos cards e falta de reinicialização imediata do ciclo de vida do Streamlit ao alternar o estado do *checkbox*.
- **Solução:** Adicionado filtro de segurança por *list comprehension* diretamente na função `tela_agenda` (`[t for t in tarefas if t.concluida]`) e inserido a instrução `st.rerun()` logo após a alteração do status da tarefa para atualizar a tela instantaneamente.

#### 🐛 Bug 7: Perda de Vínculos de Disciplinas, Alunos Matriculados e Dono da Tarefa no JSON
- **Problema:** Ao encerrar e reabrir o sistema, o salvamento no banco JSON não restaurava as disciplinas associadas aos perfis dos alunos nem a atribuição do dono original de cada tarefa.
- **Causa:** A rotina de serialização/desserialização em `persistencia.py` omitia a lista `disciplinas` do dicionário de alunos, o atributo `alunos_matriculados` das disciplinas e a propriedade `dono` nos objetos do tipo `Tarefa`.
- **Solução:** Reformulação das funções `sistema_para_dict()` e `dict_para_sistema()` em `src/utils/persistencia.py` para mapear a lista de nomes de disciplinas do aluno, a lista de matrículas vinculadas às cadeiras e a amarração bidirecional dos donos das tarefas durante o recarregamento dos dados.

#### 🐛 Bug 8: Duplicação e Acúmulo de Objetos na Memória ao Recarregar o JSON
- **Problema:** Ao chamar a desserialização do banco de dados, os novos registros lidos do arquivo JSON eram adicionados sobre os registros já existentes na memória, gerando duplicações indesejadas.
- **Causa:** Falta de reset prévio nas estruturas em memória antes do laço de recriação dos objetos.
- **Solução:** Inclusão de instruções explícitas de limpeza (`sistema.alunos_por_matricula = {}`, `sistema.disciplinas_por_nome = {}`, `sistema.postagens = []` e `sistema.eventos = []`) no início da função `dict_para_sistema()`.

#### 🐛 Bug 9: Persistência Fantasma de Dados Antigos / Localização do Banco Físico
- **Problema:** Mesmo apagando o banco de dados via interface ou tentando reiniciar o projeto, o sistema reaparecia com dados antigos gravados em execuções anteriores.
- **Causa:** O arquivo físico `dados_focusu.json` permanecia salvo na pasta raiz do projeto (`C:\Users\Ana Beatriz\Desktop\CDN\PPII\FocusU\dados_focusu.json`) sendo lido automaticamente pela função `carregar_sistema_json()`.
- **Solução:** Mapeamento do caminho absoluto do banco local no diretório do projeto, fornecendo instruções para exclusão manual/via terminal (`Remove-Item dados_focusu.json`) e criação de rotina programática para zerar o arquivo e os dicionários em memória atomicamente.

---

### 4. Ganho de Desempenho e Análise de Riscos
- **Complexidade de Tempo:** Reduzida de $O(n)$ para $O(1)$ nas verificações, buscas e exclusões no back-end.
- **Persistência Confiável:** Gravação e leitura em disco no formato JSON mantendo integridade estrutural entre sessões do usuário sem perda de atributos essenciais (senhas, fotos, matrículas e autorias).
- **Confiabilidade da Interface Gráfica:** Roteamento reativo via `st.session_state` com sincronização e atualização instantânea do estado da aplicação (`st.rerun()`).
- **Integridade dos Dados:** Validação estrita contra campos vazios, suporte a operações atômicas de exclusão em múltiplos dicionários e mutação segura via setters encapsulados nos modelos OO.