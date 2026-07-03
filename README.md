<div align="center">
  <img src="images/logo_focusu.png" alt="FocusU Logo" width="120px" style="border-radius: 20px;"/>
  
  ### *Plataforma de Organização e Interação Universitária*

  [![Python Version](https://img.shields.io/badge/Python-3.10%2B-6C5CE7?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![POO Pillars](https://img.shields.io/badge/Paradigma-POO_Avançado-A29BFE?style=for-the-badge)](https://github.com/)
  [![Status](https://img.shields.io/badge/Status-em_andamento-00B894?style=for-the-badge)](https://github.com/)

  ---
  <p align="center">
    <b>Desenvolvido por:</b><br>
     Ayra ·  Beatriz  ·  Clara Reis
  </p>
  ---
</div>

##  Sobre o Projeto

O **FocusU** é um ecossistema acadêmico completo executado via Linha de Comando (CLI), projetado para auxiliar estudantes universitários na gestão das suas rotinas de estudo, acompanhamento de disciplinas e engajamento social integrado. 

A plataforma conecta a produtividade individual (cronogramas e gerenciamento de tempo) com a colaboração coletiva através de um **Feed Inteligente**, simulando de forma robusta as interações de uma comunidade estudantil real.

---

##  Identidade Visual & Cores do Projeto

O sistema foi modelado seguindo a paleta de cores oficial da marca **FocusU**:

*  **Roxo Acadêmico (`#6C5CE7`):** Cor principal que representa o foco, sabedoria e ambiente universitário.
*  **Lavanda Claro (`#A29BFE`):** Utilizado para realces de subseções e interfaces secundárias.
*  **Verde Sucesso (`#00B894`):** Indicador de operações concluídas e cadastros bem-sucedidos.
*  **Grafite Escuro (`#2D3436`):** Base do terminal e estruturação de dados.

---

##  Funcionalidades Principais

* **Identidade e Cadastro Único:** Sistema de validação tripla em tempo real que impede a duplicidade de Matrículas, Nomes de Usuário ou E-mails corporativos.
* **Gestão de Rotinas Produtivas:** Vinculação de blocos de atividades cronometradas (em minutos) diretamente ao perfil do Aluno.
* **Grade de Disciplinas:** Permite que os alunos se matriculem em disciplinas globais criadas e lecionadas por professores cadastrados.
* **Feed Polimórfico:** Espaço centralizado de compartilhamento que processa dinamicamente múltiplos formatos de conteúdo (Postagens Gerais, Dúvidas de Disciplinas e Materiais de Estudo).
* **Mecanismo de Exclusão Segura (Anonimização):** Proteção avançada contra vazamento de memória. Ao apagar uma conta, as rotinas associadas são limpas do cache e as postagens públicas permanecem no feed de forma íntegra, convertidas automaticamente para a autoria de um *"Usuário Anônimo"*.

---

##  Pilares de POO Implementados

O FocusU foi construído como consolidação prática dos conceitos avançados de **Programação Orientada a Objetos**:

* **Abstração e Interfaces:** Contratos puros abstratos via módulo `abc` para isolamento de comportamentos obrigatórios (Interface `Publicavel`).
* **Encapsulamento Rígido:** Proteção de atributos críticos (`_nome`, `_email`, `_atividade`, `_tempo`) usando getters e setters (`@property`) com validações rigorosas de negócio.
* **Herança & Polimorfismo Avançado:** Especializações de postagens (`PostagemDuvida` e `PostagemMaterial`) redefinem o método herdado `.publicar()`. O motor do feed renderiza dinamicamente as coleções genéricas sem checagem estática de tipo (*Duck Typing*).
* **Gerenciamento de Memória (Destrutores):** Uso ativo de métodos mágicos `__del__` sincronizados com atributos estáticos de classe (`total_usuarios`, `total_postagens`) para monitorar o ciclo de vida e renderizar estatísticas exatas em tempo real.

---

## 📁 Estrutura do Repositório

```text
FocusU/
│
├── docs/               # Documentação técnica e Diagrama de Classes
│   ├── diagrama_classes.md
│   └── diario_de_bordo.md
│
├── images/             # Identidade visual e screenshots do sistema
│
├── src/                # Código-fonte principal do projeto
│   ├── interfaces/     # Contratos abstratos (publicavel.py)
│   ├── models/         # Entidades de negócio (usuario.py, postagem.py, etc.)
│   ├── system/         # Core / Gerenciador centralizado (sistema.py)
│   └── main.py         # Arquivo de entrada do programa
│
├── tests/              # Suíte de testes automatizados
├── requirements.txt    # Dependências do projeto
└── .gitignore          # Arquivos ignorados pelo controle de versão
```

##  Como Executar o Projeto

Siga os passos abaixo para clonar o repositório, configurar o ambiente local e executar o sistema **FocusU 2.0** na sua máquina.

### Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em seu computador:
* **Python 3.10** ou versão superior.
* **Git** (opcional, utilizado para clonar o repositório via terminal).

---

###  Passo a Passo

#### 1. Clonar o Repositório
Abra o seu terminal (Prompt de Comando, PowerShell ou Terminal do Linux/Mac) e execute o comando abaixo para clonar o projeto:
```bash
git clone [https://github.com/seu-usuario/FocusU.git](https://github.com/seu-usuario/FocusU.git)
```
2. Acessar o Diretório do Projeto

Navegue para dentro da pasta raiz do projeto que foi criada após a clonagem:

```bash
cd FocusU
```
3. Executar a Aplicação

Para iniciar a interface em linha de comando (CLI) do sistema, execute o arquivo principal localizado dentro da pasta `src/` a partir da raiz do repositório:
* No Windows:
```Bash
python src/main.py
```
* No Linux/macOS:
```Bash
python3 src/main.py
```
##  Resolução de Problemas Comuns
* Erro de Importação (ModuleNotFoundError):

O arquivo `src/main.py` já possui uma blindagem que adiciona automaticamente a pasta raiz ao `sys.path`. Certifique-se de executar o comando de inicialização sempre a partir da raiz do repositório `(/FocusU)` e nunca navegando para dentro da pasta `/src`.

* Versão Incorreta do Python:

Certifique-se de que o comando `python --version` ou `python3 --version` retorna uma versão 3.10.x ou superior. Versões antigas podem apresentar problemas com métodos mágicos ou validações estáticas específicas utilizadas no sistema.