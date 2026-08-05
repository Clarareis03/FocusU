## Refatoração de Estruturas de Dados, Persistência JSON e Interface Web

**Responsável:** Ana Beatriz  
**Data de Conclusão:** 24/07/2026 *(Atualizado em 04/08/2026 com módulos de rastreio de rotina, privacidade e gerenciamento de perfil)*  

---

### 1. Mapeamento de Gargalos e Objetivos
*   Foi mapeada a presença de buscas lineares O(n) nas rotinas de validação de duplicidade de alunos (matrícula e e-mail) e disciplinas. Em cenários com muitos registros, o tempo de checagem crescia de forma proporcional ao número de elementos cadastrados.
*   Houve a necessidade de integrar a lógica Orientada a Objetos (OO) do back-end com uma interface gráfica em **Streamlit**, criando telas para o gerenciamento de alunos, disciplinas e a **Agenda de Tarefas**.
*   **Mecanismo de Persistência de Dados:** Implementação e aprimoramento de um sistema de salvamento/carregamento local via arquivo JSON (`dados_focusu.json`) para garantir a permanência de cadastros, postagens, eventos e tarefas entre reinicializações do servidor Web.
*   **Aprimoramento de Autonomia e Privacidade (Novo):** Necessidade de dar aos alunos maior controle sobre seus próprios dados na interface, permitindo registrar tempo de estudo automatizado, cancelar matrículas ativas, apagar as próprias postagens e visualizar apenas tarefas de sua autoria na Agenda.

---

### 2. Alterações de Estrutura e Orientação a Objetos
*   **Dicionários (Tabela Hash O(1)):** As listas simples foram substituídas por dicionários (`dict`), utilizando chaves únicas para buscas diretas:
    *   `alunos_por_matricula`: Indexado pela matrícula do aluno.
    *   `alunos_por_email`: Indexado pelo e-mail do aluno (em caixa baixa).
    *   `disciplinas_por_nome`: Indexado pelo nome normalizado da disciplina.
*   **Encapsulamento na Classe `Tarefa`:** Utilização de propriedades privadas (`_concluida`, `_titulo`, etc.) expostas via `@property` e `@setter` para garantir consistência de dados e controle de mutação na interface.
*   **Integração do Modelo `Rotina` (Novo):** A classe `Rotina` foi conectada à interface `tela_agenda` e `tela_alunos`. Agora, a conclusão de uma tarefa ou o preenchimento manual gera uma nova instância de `Rotina` salva diretamente no perfil do aluno, acumulando o tempo total de estudos.
*   **Camada de Persistência em JSON (`src/utils/persistencia.py`):**
    *   Implementação das funções `sistema_para_dict()` (serialização) e `dict_para_sistema()` (desserialização) para conversão bidirecional.
    *   Mapeamento e preservação de atributos complexos como: senhas salvas, fotos em Base64, rotinas individuais de estudos, autorias de postagens/comentários e lista de alunos matriculados por disciplina.

---

### 3. Erros Encontrados e Soluções

Durante o desenvolvimento, execução dos testes, integração com o Streamlit e refatoração da persistência de dados, surgiram os seguintes problemas e soluções:

#### 🐛 Bug 1: Duplicidade por Variação de Acentuação e Maiúsculas
*   **Problema:** O sistema permitia cadastrar "Análise de Dados" e "analise de dados" como duas disciplinas distintas, pois as strings geravam hashes diferentes.
*   **Solução:** Implementação do método `_normalizar_chave()` no `sistema.py` usando a biblioteca nativa `unicodedata` para remover acentos, converter o texto para minúsculas e aplicar `.strip()`.

#### 🐛 Bug 2: Entradas Inválidas Derrubando o Menu Terminal (`main.py`)
*   **Problema:** Ao digitar letras onde se esperava números, o Python disparava erros e encerrava o programa.
*   **Solução:** Adicionado um conjunto `OPCOES_VALIDAS` para pré-checagem e blindagem global com bloco `try/except`.

#### 🐛 Bug 3: Inconsistência ao Remover Aluno de Múltiplas Chaves
*   **Problema:** Ao apagar uma conta de aluno, a chave da matrícula era removida, mas a chave de e-mail permanecia cadastrada.
*   **Solução:** Atualização do método `remover_aluno()` para limpar atomicamente a chave correspondente em ambos os dicionários.

#### 🐛 Bug 4: Omissão da Agenda no Roteamento do Menu Lateral (`interface_web.py`)
*   **Problema:** A funcionalidade de Agenda foi criada, mas não aparecia na barra de navegação gráfica.
*   **Solução:** Atualização do `interface_web.py` com a importação da função e roteamento correto.

#### 🐛 Bug 5: Violabilidade/Falta de Setter no Encapsulamento (`AttributeError`)
*   **Problema:** Ao desmarcar a caixinha de uma tarefa concluída, a aplicação encerrava com erro por falta de setter.
*   **Solução:** Adição do decorator `@concluida.setter` na classe `Tarefa`.

#### 🐛 Bug 6: Ineficiência de Filtragem Dinâmica por Status na Interface Web
*   **Problema:** Ao selecionar o filtro "Concluídas", tarefas pendentes continuavam sendo renderizadas.
*   **Solução:** Adicionado filtro de segurança por *list comprehension* diretamente na função `tela_agenda` e inserido a instrução `st.rerun()`.

#### 🐛 Bug 7: Perda de Vínculos de Disciplinas, Alunos Matriculados e Dono da Tarefa no JSON
*   **Problema:** O salvamento no banco JSON não restaurava as disciplinas associadas aos perfis dos alunos nem a atribuição do dono original de cada tarefa.
*   **Solução:** Reformulação das funções de persistência para mapear a lista de nomes de disciplinas do aluno, matrículas vinculadas e amarração bidirecional dos donos das tarefas.

#### 🐛 Bug 8: Duplicação e Acúmulo de Objetos na Memória ao Recarregar o JSON
*   **Problema:** Os novos registros lidos do arquivo JSON eram adicionados sobre os registros já existentes na memória.
*   **Solução:** Inclusão de instruções explícitas de limpeza no início da função `dict_para_sistema()`.

#### 🐛 Bug 9: Persistência Fantasma de Dados Antigos
*   **Problema:** Mesmo apagando o banco de dados via interface, o sistema reaparecia com dados antigos gravados em execuções anteriores.
*   **Solução:** Mapeamento do caminho absoluto do banco local no diretório do projeto para deleção correta.

#### 🐛 Bug 10: Vazamento de Tarefas entre Usuários (Falta de Privacidade)
*   **Problema:** A tela de Agenda mostrava todas as tarefas criadas em uma disciplina para todos os alunos matriculados nela, como se fosse uma agenda pública.
*   **Solução:** Implementação de um filtro rigoroso no laço de renderização da `tela_agenda`, exibindo as tarefas apenas se o atributo `dono` for correspondente à matrícula do aluno ativo na sessão (`aluno_logado.matricula`).

#### 🐛 Bug 11: Tarefas Concluídas Não Refletiam no Tempo de Estudo
*   **Problema:** Concluir uma tarefa na Agenda apenas mudava seu status visual, sem registrar quanto tempo o aluno se dedicou àquela atividade.
*   **Solução:** Substituição do botão simples de conclusão por uma interface composta (input numérico + botão). Ao concluir, o sistema agora captura o tempo digitado e automaticamente vincula uma nova `Rotina` ao perfil do aluno.

#### 🐛 Bug 12: Prisão de Dados (Impossibilidade de Gerenciamento Próprio)
*   **Problema:** Alunos matriculados erroneamente em uma disciplina não conseguiam sair dela, e posts publicados com erro no Feed não podiam ser excluídos pelo criador.
*   **Solução:** Adicionada a seção "Minhas Matrículas Ativas" com botões dinâmicos para desmatricular e uma verificação de autoridade no Feed que exibe o botão "Apagar Postagem" unicamente para o dono do post.

#### 🐛 Bug 13: Ausência de Mecanismo de Recuperação de Acesso
*   **Problema:** Usuários que esqueciam a senha ficavam bloqueados para sempre, pois a interface não possuía rota de redefinição.
*   **Solução:** Inclusão da aba "Esqueci a Senha" na área de login, validando os dados cruzados (e-mail e matrícula) para permitir a sobrescrita segura da senha.

---

### 4. Ganho de Desempenho e Análise de Riscos
*   **Complexidade de Tempo:** Reduzida de O(n) para O(1) nas verificações, buscas e exclusões no back-end.
*   **Persistência Confiável:** Gravação e leitura em disco no formato JSON mantendo integridade estrutural entre sessões do usuário sem perda de atributos essenciais (senhas, fotos, matrículas e autorias).
*   **Confiabilidade da Interface Gráfica:** Roteamento reativo via `st.session_state` com sincronização e atualização instantânea do estado da aplicação (`st.rerun()`).
*   **Integridade dos Dados:** Validação estrita contra campos vazios, suporte a operações atômicas de exclusão em múltiplos dicionários e mutação segura via setters encapsulados nos modelos OO.
*   **Experiência e Retenção do Usuário (Novo):** A autonomia entregue pelas funções de desmatricular, recuperar senha, apagar posts e o gamification gerado pela contagem de horas estudadas reduzem a dependência de suporte técnico e incentivam a utilização diária e confiável do sistema por parte dos alunos.