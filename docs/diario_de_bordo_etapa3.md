## Refatoração de Estruturas de Dados e Implementação da Interface Web

**Responsável:** Ana Beatriz  
**Data de Conclusão:** 24/07/2026  

---

### 1. Mapeamento de Gargalos e Objetivos
- Foi mapeada a presença de buscas lineares $O(n)$ nas rotinas de validação de duplicidade de alunos (matrícula e e-mail) e disciplinas. Em cenários com muitos registros, o tempo de checagem crescia de forma proporcional ao número de elementos cadastrados.
- Houve a necessidade de integrar a lógica Orientada a Objetos (OO) do back-end com uma interface gráfica em **Streamlit**, criando telas para o gerenciamento de alunos, disciplinas e a **Agenda de Tarefas**.

---

### 2. Alterações de Estrutura e Orientação a Objetos
- **Dicionários (Tabela Hash $O(1)$):** As listas simples foram substituídas por dicionários (`dict`), utilizando chaves únicas para buscas diretas:
  - `alunos_por_matricula`: Indexado pela matrícula do aluno.
  - `alunos_por_email`: Indexado pelo e-mail do aluno (em caixa baixa).
  - `disciplinas_por_nome`: Indexado pelo nome normalizado da disciplina.
- **Encapsulamento na Classe `Tarefa`:** Utilização de propriedades privadas (`_concluida`, `_titulo`, etc.) expostas via `@property` e `@setter` para garantir consistência de dados e controle de mutação na interface.

---

### 3. Erros Encontrados e Soluções

Durante o desenvolvimento, execução dos testes e integração com o Streamlit, surgiram os seguintes problemas e soluções:

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

---

### 4. Ganho de Desempenho e Análise de Riscos
- **Complexidade de Tempo:** Reduzida de $O(n)$ para $O(1)$ nas verificações, buscas e exclusões no back-end.
- **Confiabilidade da Interface Gráfica:** Roteamento reativo via `st.session_state` com sincronização imediata de dados em memória.
- **Integridade dos Dados:** Validação estrita contra campos vazios e mutação segura via setters encapsulados nos modelos OO.