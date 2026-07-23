## Implementação de Recursão e Tratamento de Erros de Execução

**Responsável:** Ayra   
**Data de Conclusão:** 22/07/2026  

---

### 1. Mapeamento da Necessidade
Para atender ao requisito de algoritmo recursivo na plataforma FocusU e fornecer métricas de estudo aos alunos sem o uso de laços tradicionais (`for` ou `while`), foi identificada a oportunidade de processar o tempo acumulado de estudos das rotinas diretamente no modelo do aluno.

### 2. Alterações de Estrutura
- **Método Recursivo no Modelo (`models/usuario.py`):** Criado o método `calcular_tempo_estudo_recursivo()` dentro da classe `Aluno`. O algoritmo percorre a lista de rotinas de forma encadeada (soma do elemento do índice atual + chamada recursiva para `indice + 1`) até atingir o caso base (fim da lista).
- **Separação de Responsabilidades (POO):** O cálculo foi inserido na classe `Aluno` (e não no `SistemaFocusU`), mantendo o encapsulamento, pois a lista de rotinas pertence à própria instância do aluno.
- **Nova Opção no Menu (`main.py` / `focus_u.ipynb`):** Adicionada a **Opção 13** para acionar a métrica e exibir os minutos totais e as horas formatadas.

---

### 3. Erros Encontrados e Soluções 

Durante a execução dos testes e conversão para o ambiente Jupyter Notebook, surgiram os seguintes problemas:

#### 🐛 Bug 1: Falha na Instanciação da Classe Abstrata (`TypeError`)
- **Problema:** O console exibia a mensagem `Can't instantiate abstract class Aluno without an implementation for abstract method 'exibir_perfil'`.
- **Causa:** A classe mãe `UsuarioBase` definia o método `@abstractmethod exibir_perfil()`. Por inconsistência no nome ou falta de execução da célula no Notebook, o Python interpretou que a subclasse `Aluno` não cumpria o contrato obrigatório.
- **Solução:** Reimplementação garantida do método `exibir_perfil()` na classe `Aluno` e reordenação da execução das células no Jupyter Notebook para atualização da classe na memória.

#### 🐛 Bug 2: Incompatibilidade de Tipos no Algoritmo Recursivo (`TypeError` / `ValueError`)
- **Problema:** Ao tentar somar o tempo das rotinas na opção de estatística, a recursão quebrava ao encontrar entradas contendo texto (ex: `"2h"` ou `"30min"`), pois o Python não realiza operação aritmética entre inteiros e strings.
- **Causa:** Ausência de tipagem rígida ou tratamento local no momento do cálculo dos minutos.
- **Solução:** Aplicação de **Programação Defensiva** dentro da própria função recursiva usando bloco `try/except` local. Se o tempo de uma rotina não puder ser convertido para `int`, o sistema exibe um aviso orientativo, assume `0` para aquela rotina específica e **não interrompe** o cálculo das demais rotinas do aluno.

#### 🐛 Bug 3: Exibição de Mensagens Técnicas do Motor Python (`invalid literal for int()`)
- **Problema:** Ao digitar uma opção ou tempo inválido, a mensagem tratada exibia o texto original em inglês emitido pela linguagem entre parênteses (`invalid literal for int() with base 10`).
- **Causa:** O bloco `except ValueError as erro_val` repassava a string bruta do erro direto para o `print()`.
- **Solução:** Captura e tratamento condicional das mensagens no `main.py`. Erros de conversão numérica foram substituídos por mensagens amigáveis em português (ex: *"Por favor, digite apenas números inteiros sem letras"*), melhorando a experiência do usuário (UX).

---

### 4. Ganho de Desempenho e Análise de Riscos
- **Complexidade de Tempo:** $O(n)$, onde $n$ é o número de rotinas cadastradas no perfil do aluno.
- **Tolerância a Falhas:** A recursão tornou-se resiliente a dados corrompidos ou mal formatados no histórico do aluno.
- **Desacoplamento e Prontidão para Streamlit:** A lógica recursiva está 100% isolada na regra de negócio (`Aluno`), permitindo que a futura interface gráfica apenas chame o método ao clicar em um botão visual, sem necessidade de refatorar a lógica.
