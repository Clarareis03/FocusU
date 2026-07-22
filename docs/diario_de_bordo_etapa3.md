## Refatoração de Estruturas de Dados para Tabela Hash

**Responsável:** Ana Beatriz   
**Data de Conclusão:** 22/07/2026  

---

### 1. Mapeamento de Gargalos
Foi mapeada a presença de buscas lineares $O(n)$ nas rotinas de validação de duplicidade de alunos (matrícula e e-mail) e disciplinas. Em cenários com muitos registros, o tempo de checagem crescia de forma proporcional ao número de elementos cadastrados.

### 2. Alterações de Estrutura
As listas simples foram substituídas por dicionários (`dict`), utilizando chaves únicas para buscas diretas:
- `alunos_por_matricula`: Indexado pela matrícula do aluno.
- `alunos_por_email`: Indexado pelo e-mail do aluno (em caixa baixa).
- `disciplinas_por_nome`: Indexado pelo nome normalizado da disciplina.

---

### 3. Erros Encontrados e Soluções 

Durante o desenvolvimento e execução das baterias de testes, surgiram os seguintes problemas:

#### 🐛 Bug 1: Duplicidade por Variação de Acentuação e Maiúsculas
- **Problema:** O sistema permitia cadastrar "Análise de Dados" e "analise de dados" como duas disciplinas distintas, pois as strings geravam hashes diferentes.
- **Causa:** Comparação exata de caracteres na chave do dicionário.
- **Solução:** Implementação do método `_normalizar_chave()` no `sistema.py` usando a biblioteca nativa `unicodedata` para remover acentos, converter o texto para minúsculas e aplicar `.strip()`.

#### 🐛 Bug 2: Entradas Inválidas Derrubando o Menu (`main.py`)
- **Problema:** Ao digitar letras onde se esperava números de opção ou ao selecionar índices inexistentes na lista, o Python disparava `ValueError` ou `IndexError` e encerrava a execução do programa.
- **Solução:** Adicionado um conjunto `OPCOES_VALIDAS` para pré-checagem em $O(1)$ no menu e blindagem global com bloco `try/except` capturando `ValueError` e `IndexError` graciosamente.

#### 🐛 Bug 3: Inconsistência ao Remover Aluno de Múltiplas Chaves
- **Problema:** Ao apagar uma conta de aluno, a chave da matrícula era removida do dicionário, mas a chave de e-mail permanecia cadastrada, impedindo novo cadastro com aquele e-mail.
- **Solução:** Atualização do método `remover_aluno()` para limpar atomicamente a chave correspondente em ambos os dicionários (`alunos_por_matricula` e `alunos_por_email`).

---

### 4. Ganho de Desempenho e Análise de Riscos
- **Complexidade de Tempo:** Reduzida de $O(n)$ para $O(1)$ nas verificações e exclusões.
- **Colisões de Hash:** Gerenciadas de forma transparente pelo Python via *Open Addressing*.
- **Integridade da Interface:** Para listagem no console ou interface gráfica, foi mantida a iteração através do método `.values()`, preservando a facilidade de exibição dos objetos.