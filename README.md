<div align="center">
  <img src="images/logo_focusu.png" alt="FocusU Logo" width="120px" style="border-radius: 20px;"/>
  
  ### *Plataforma de Organização, Interação e Rede Social Universitária*

  [![Python Version](https://img.shields.io/badge/Python-3.10%2B-6C5CE7?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![POO Pillars](https://img.shields.io/badge/Paradigma-POO_Avançado-A29BFE?style=for-the-badge)](https://github.com/)
  [![Status](https://img.shields.io/badge/Status-concluído-00B894?style=for-the-badge)](https://github.com/)

  ---
  <p align="center">
    <b>Desenvolvido por:</b><br>
     Ayra ·  Beatriz  ·  Clara Reis
  </p>
  ---
</div>

## 📌 Sobre o Projeto

O **FocusU** é um ecossistema acadêmico completo com **interface web interativa em Streamlit**, projetado para auxiliar estudantes universitários na gestão da sua rotina de estudos, acompanhamento de disciplinas e engajamento social.

A plataforma conecta a organização individual com a colaboração coletiva através de um **Feed estilo Instagram** com fotos e comentários em tempo real, além de um **Dashboard de Estatísticas** completo para acompanhamento de métricas de engajamento da comunidade.

---

## 🎨 Identidade Visual & Cores do Projeto

O sistema foi modelado seguindo a paleta de cores oficial e o design dark mode do **FocusU**:

* **Roxo Acadêmico (`#6C5CE7`):** Cor principal que representa o foco, sabedoria e ambiente universitário.
* **Lavanda Claro (`#A29BFE`):** Utilizado para realces de subseções e interfaces secundárias.
* **Verde Sucesso (`#00B894`):** Indicador de operações concluídas e cadastros bem-sucedidos.
* **Grafite / Dark Mode (`#121214` & `#2D3436`):** Base da interface web e estruturação dos cards no feed.

---

## 🚀 Funcionalidades Principais

* **Identidade e Cadastro Único:** Validação em tempo real que impede a duplicidade de Matrículas, Nomes de Usuário ou E-mails corporativos.
* **Gestão de Alunos e Disciplinas:** Cadastro centralizado com suporte a upload de fotos de perfil (Base64) e vínculo de professores às disciplinas.
* **📸 Feed estilo Instagram:**
  * Postagens com upload de fotos no formato card escuro centralizado.
  * Suporte a múltiplos tipos de postagem (Geral, Dúvidas de Disciplina, Materiais de Estudo e Eventos).
  * Sistema de curtidas (`❤️`) e comentários em linha com seleção do usuário que está comentando.
* **📊 Dashboard & Estatísticas:**
  * Métricas em tempo real (KPIs de alunos, postagens, curtidas e comentários).
  * Gráfico interativo da distribuição de tipos de publicação.
  * Ranking dos autores mais ativos e destaque para a publicação mais engajada da comunidade.
* **Mecanismo de Exclusão Segura (Anonimização):** Proteção avançada. Ao remover uma conta, o cache de rotinas é limpo e as postagens públicas permanecem integras no feed convertidas para *"Usuário Anônimo"*.

---

## 🧠 Pilares de POO Implementados

O FocusU foi construído como consolidação prática dos conceitos avançados de **Programação Orientada a Objetos**:

* **Abstração e Interfaces:** Contratos abstratos via módulo `abc` para isolamento de comportamentos obrigatórios (Interface `Publicavel`).
* **Encapsulamento Rígido:** Proteção de atributos críticos (`_nome`, `_email`, `_matricula`, `_titulo`) usando getters e setters (`@property`) com validações rigorosas.
* **Herança & Polimorfismo Avançado:** Especializações de postagens (`PostagemDuvida` e `PostagemMaterial`) e eventos (`Evento`) com renderização dinâmica genérica (*Duck Typing*).
* **Gerenciamento de Memória & Estado:** Uso ativo de destruidores e métodos mágicos sincronizados com o estado global da aplicação web.

---

## 📁 Estrutura do Repositório

```text
FocusU/
│
├── docs/                 # Documentação técnica e Diagrama de Classes
│   ├── diagrama_classes.md
│   └── diario_de_bordo.md
│
├── images/               # Identidade visual e screenshots do sistema
│
├── src/                  # Código-fonte principal do projeto
│   ├── interfaces/       # Contratos abstratos (publicavel.py)
│   ├── models/           # Entidades de negócio (usuario.py, postagem.py, evento.py)
│   ├── system/           # Gerenciador centralizado da aplicação (sistema.py)
│   ├── utils/            # Funções auxiliares (helpers de imagem Base64)
│   └── web/              # Interface Web em Streamlit (interface_web.py e paginas.py)
│
├── requirements.txt      # Dependências da aplicação
└── README.md             # Documentação oficial do projeto
```

## 💻 Como Executar o Projeto
Siga os passos abaixo para clonar o repositório, configurar o ambiente local e rodar a aplicação web do FocusU.

Pré-requisitos
Python 3.10 ou versão superior.

Git instalado.

### ⚙️ Passo a Passo
1. Clonar o Repositório

```Bash
git clone [https://github.com/seu-usuario/FocusU.git](https://github.com/seu-usuario/FocusU.git)
cd FocusU
```
### 2. Instalar as Dependências
Certifique-se de instalar as bibliotecas necessárias (Streamlit, Pandas, etc.):

```Bash
pip install -r requirements.txt
```

### 3. Executar a Aplicação Web
Execute a interface web no navegador rodando o comando a partir da raiz do repositório:

No Windows / Linux / macOS:

```Bash
streamlit run src/web/interface_web.py
A aplicação abrirá automaticamente no seu navegador no endereço http://localhost:8501.
```

## 🛠️ Resolução de Problemas Comuns
ModuleNotFoundError (NameError ou Erro de Importação):
Certifique-se de rodar o comando streamlit run sempre estando na raiz da pasta /FocusU.

Erro de carregamento das imagens:
As imagens de perfil e dos posts são convertidas em cadeias Base64. Certifique-se de enviar arquivos nos formatos válidos (.jpg, .jpeg ou .png).