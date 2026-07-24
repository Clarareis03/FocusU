## Implementação da Interface Web e Deploy da Aplicação (Streamlit)

**Responsável:** Clara Reis  
**Data de Conclusão:** 24/07/2026  

---

### 1. Mapeamento da Necessidade
Para evoluir o projeto além da Linha de Comando (CLI) e proporcionar uma experiência de usuário moderna, responsiva e acessível por navegador, foi identificada a oportunidade de construir uma interface gráfica completa em **Streamlit**. O objetivo foi unificar a gestão de alunos, disciplinas e estatísticas, além de transformar a interação social em um **Feed estilo Instagram** com fotos e comentários em tempo real.

---

### 2. Alterações de Estrutura
- **Criação do Módulo Web (`src/web/`):** Criados os arquivos `interface_web.py` (roteador principal e menu lateral/sidebar) e `paginas.py` (renderização individual de cada tela), mantendo o `main.py` da CLI 100% intacto.
- **Integração sem Duplicação (POO):** As páginas consomem diretamente a instância global do `SistemaFocusU` armazenada no estado da sessão (`st.session_state`). Todas as regras de negócio, contratos e validações desenvolvidas nos modelos originais foram mantidas e reutilizadas.
- **Feed Interativo Multimídia (`paginas.py`):** Reformulação do feed para exibir postagens e eventos em cards centralizados no modo escuro (Dark Mode). Adicionados suporte a upload de fotos de capa/posts, filtro por tipo (Geral, Dúvidas, Materiais e Eventos), sistema de curtidas e caixa de comentários com seleção de autor.
- **Dashboard de Estatísticas & KPIs (`paginas.py`):** Construção de um painel analítico exibindo métricas gerais (KPIs de alunos, posts, curtidas e comentários), gráfico de distribuição de conteúdos via Pandas/Plotly e destaques da comunidade.
- **Arquivos de Configuração (`requirements.txt` e `README.md`):** Mapeamento das dependências essenciais (`streamlit`, `pandas`, `Pillow`, `plotly`) e atualização completa da documentação com instruções de execução via web.

---

### 3. Erros Encontrados e Soluções 

Durante o desenvolvimento da interface e o processo de hospedagem no **Streamlit Community Cloud**, surgiram os seguintes problemas:

#### 🐛 Bug 1: Quebra do Layout do Feed e Identificação de Autoria nos Comentários
- **Problema:** Os comentários apareciam dentro de caixas brancas desconfiguradas (`st.expander`), exibindo o autor fixo como "Anônimo" e quebrando o padrão estético do Instagram.
- **Causa:** O método original `.comentar("texto")` apenas armazenava uma string simples no post sem registrar a entidade do aluno que comentou, além da limitação visual dos componentes nativos do Streamlit.
- **Solução:** Reestruturação da área de comentários em HTML/CSS customizado linha a linha (avatar + nome em negrito + texto lado a lado) e adição de um seletor dinâmico (`st.selectbox`) para escolher qual aluno está comentando. O comentário passou a ser persistido no formato `Autor::Texto` para renderização correta.

#### 🐛 Bug 2: Ausência de Módulos no Servidor do Streamlit Cloud (`ModuleNotFoundError`)
- **Problema:** Ao realizar o deploy no Streamlit Cloud, o aplicativo falhava na inicialização com a mensagem `No module named 'plotly'` no log da plataforma.
- **Causa:** As bibliotecas utilitárias de gráficos e manipulação de imagem usadas no front-end não estavam listadas no arquivo `requirements.txt` da raiz do repositório.
- **Solução:** Atualização do `requirements.txt` incluindo `plotly`, `pandas`, `Pillow` e `streamlit` com versões mínimas compatíveis, forçando o servidor da nuvem a instalar todas as dependências durante o build.

#### 🐛 Bug 3: Falha de Resolução de Caminhos e Módulos do Python (`ModuleNotFoundError: No module named 'paginas'`)
- **Problema:** Ao rodar a aplicação hospedada a partir do caminho `src/web/interface_web.py`, o Python no servidor remoto não localizava as pastas internas do projeto (`src/`, `web/` ou `system/`).
- **Causa:** Divergência entre o diretório de execução do servidor do Streamlit Cloud (que roda a partir da raiz `/mount/src/focusu/`) e a estrutura interna de subpastas do repositório.
- **Solução:** Implementação de ajuste dinâmico no topo do `interface_web.py` usando `Path` e `sys.path.insert()`. As variáveis `PROJECT_ROOT`, `SRC_DIR` e `WEB_DIR` foram adicionadas explicitamente ao `sys.path`, garantindo que todas as importações relativas funcionem perfeitamente tanto localmente quanto na nuvem.

---

### 4. Ganho de Desempenho e Análise de Riscos
- **Acessibilidade e UX:** Transformação de uma aplicação estática de terminal em uma Web App responsiva, interativa e acessível via URL pública no navegador.
- **Isolamento de Camadas:** Total desacoplamento entre a camada de apresentação (`src/web/`) e o núcleo de regras de negócio (`src/system/` e `src/models/`), respeitando rigorosamente os princípios de POO.
- **Persistência de Estado na Sessão:** Uso otimizado do `st.session_state` mantendo as instâncias de memória vivas durante toda a navegação do usuário sem necessidade de reprocessar o sistema a cada clique.