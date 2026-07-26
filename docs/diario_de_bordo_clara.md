# 📓 Diário de Bordo — Projeto FocusU

> **Projeto:** FocusU — Plataforma de Organização Universitária  
> **Desenvolvedor(a):** Clara Reis  

---

## 📌 Visão Geral do Projeto
O **FocusU** é uma aplicação web desenvolvida em Python (Streamlit) para auxiliar estudantes universitários na gestão de rotinas de estudo, disciplinas, tarefas e engajamento acadêmico.

---

## 📋 Registros de Desenvolvimento

### 🔹 Etapa 1: Configuração Inicial e Estrutura do Projeto
* **Objetivo:** Configurar o repositório, ambiente de desenvolvimento e arquitetura base da aplicação.
* **O que foi feito:**
  - Criação e estruturação de pastas do repositório (`src/`, `src/web/`, `src/utils/`).
  - Configuração do ambiente virtual e instalação das dependências base.
  - Implementação da interface web inicial utilizando o framework Streamlit.
* **Desafios / Bloqueios:**
  - Dificuldade inicial com a resolução de imports de módulos em Python (`ModuleNotFoundError`).
* **Solução:**
  - Padronização das rotas de importação e ajuste na estrutura de pacotes internos em `src/`.

---

### 🔹 Etapa 2: Implementação da Persistência de Dados (JSON)
* **Objetivo:** Criar um mecanismo para salvar e carregar os dados de alunos, disciplinas e postagens em arquivo local.
* **O que foi feito:**
  - Criação do módulo `persistencia.py` para serialização e desserialização de objetos.
  - Leitura e gravação de dados estruturados em formato `.json`.
  - Integração do carregamento de dados ao `st.session_state` do Streamlit.
* **Desafios / Bloqueios:**
  - Inconsistência na localização do arquivo JSON entre o ambiente local e a nuvem do Streamlit Cloud.
* **Solução:**
  - Definição do caminho do arquivo como caminho absoluto na raiz do projeto (`PROJECT_ROOT` via `pathlib.Path`).

---

### 🔹 Etapa 3: Sistema de Autenticação e Gestão de Perfil
* **Objetivo:** Desenvolver as telas e rotinas de cadastro, login e gerenciamento da sessão do aluno.
* **O que foi feito:**
  - Implementação das abas de **Entrar** e **Criar Conta**.
  - Criação do formulário com validação de campos obrigatórios (nome, e-mail, matrícula e senha).
  - Tratamento de imagens de perfil via upload e conversão para formato Base64.
* **Desafios / Bloqueios:**
  - Falhas no login causadas por espaços adicionais no final dos campos e incompatibilidade na gravação de dados antigos sem senha.
* **Solução:**
  - Padronização do tratamento dos dados com `.strip()` e conversão explícita para string, forçando o salvamento imediato após a gravação da senha.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python 3.x
* **Framework Web:** Streamlit
* **Armazenamento Local:** JSON
* **Controle de Versão:** Git & GitHub
* **Hospedagem / Implantação:** Streamlit Cloud

---

## 🚀 Próximos Passos (Backlog)
- [ ] Adicionar funcionalidade de filtro e busca de disciplinas.
- [ ] Criar visualização gráfica para estatísticas de tempo de estudo.
- [ ] Implementar exportação de relatórios acadêmicos.
- [ ] Conectar a aplicação a um banco de dados em nuvem permanente (ex: Supabase / PostgreSQL).