from pathlib import Path
import sys

# Configura os caminhos absolutos dos diretórios no sistema
WEB_DIR = Path(__file__).resolve().parent
SRC_DIR = WEB_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

# Adiciona todas as pastas chave no sys.path
for path in [PROJECT_ROOT, SRC_DIR, WEB_DIR]:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

import streamlit as st

# Importando via estrutura de pastas do projeto
from src.web.css import carregar_css
from src.web.paginas import (
    tela_agenda,
    tela_alunos,
    tela_disciplinas,
    tela_estatisticas,
    tela_feed,
    tela_home,
)
from src.system.sistema import SistemaFocusU

# Importa as funções do arquivo persistencia.py localizado na pasta utils
try:
    from src.utils.persistencia import carregar_sistema_json, salvar_sistema_json
except ModuleNotFoundError:
    try:
        from utils.persistencia import carregar_sistema_json, salvar_sistema_json
    except ModuleNotFoundError:
        from persistencia import carregar_sistema_json, salvar_sistema_json

# Configuração da página
st.set_page_config(page_title="FocusU", page_icon="🎓", layout="wide")

# Aplica o CSS
st.markdown(carregar_css(), unsafe_allow_html=True)

# Inicializa e carrega o sistema do banco JSON
if "sistema" not in st.session_state:
    instancia_sistema = SistemaFocusU()
    st.session_state.sistema = carregar_sistema_json(instancia_sistema)

# Inicializa variáveis de sessão essenciais
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "aluno_logado" not in st.session_state:
    st.session_state.aluno_logado = None

if "recuperando_senha" not in st.session_state:
    st.session_state.recuperando_senha = False

if "cadastrando" not in st.session_state:
    st.session_state.cadastrando = False

# Define as variáveis utilizadas pelo restante da interface
sistema = st.session_state.sistema
ASSETS_DIR = WEB_DIR / "assets"

# ==========================================================
# TELA DE LOGIN / CADASTRO / RECUPERAÇÃO DE SENHA
# ==========================================================
if st.session_state.aluno_logado is None:
    # Tenta importar a classe Aluno para podermos criar novas contas
    try:
        from src.models.usuario import Aluno
    except ModuleNotFoundError:
        try:
            from models.usuario import Aluno
        except ModuleNotFoundError:
            from usuario import Aluno

    # Centraliza o conteúdo visualmente
    col_vazia1, col_login, col_vazia2 = st.columns([1, 2, 1])
    
    with col_login:
        st.markdown("<h1 style='text-align: center;'>🎓 FocusU</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Plataforma Acadêmica</p>", unsafe_allow_html=True)
        st.divider()

        # FLUXO 1: TELA DE RECUPERAÇÃO DE SENHA
        if st.session_state.recuperando_senha:
            st.subheader("Recuperação de Senha")
            st.info("Para redefinir sua senha, confirme seus dados de cadastro.")
            
            recup_email = st.text_input("Seu E-mail cadastrado")
            recup_matricula = st.text_input("Sua Matrícula")
            nova_senha = st.text_input("Digite a Nova Senha", type="password")
            
            col3, col4 = st.columns(2)
            with col3:
                if st.button("Redefinir Senha", type="primary", use_container_width=True):
                    if not recup_email or not recup_matricula or not nova_senha:
                        st.warning("Preencha todos os campos!")
                    else:
                        if sistema.redefinir_senha(recup_email, recup_matricula, nova_senha):
                            salvar_sistema_json(sistema)
                            st.success("Senha atualizada! Você já pode fazer login.")
                            st.session_state.recuperando_senha = False
                            st.rerun()
                        else:
                            st.error("Dados incorretos. Verifique e-mail e matrícula.")
            
            with col4:
                if st.button("Voltar ao Login", use_container_width=True):
                    st.session_state.recuperando_senha = False
                    st.rerun()

        # FLUXO 2: TELA DE CADASTRO DE NOVA CONTA
        elif st.session_state.cadastrando:
            st.subheader("Criar Nova Conta")
            
            cad_nome = st.text_input("Nome Completo")
            cad_email = st.text_input("E-mail")
            cad_mat = st.text_input("Matrícula")
            cad_senha = st.text_input("Senha", type="password")
            
            col_cad1, col_cad2 = st.columns(2)
            with col_cad1:
                if st.button("Finalizar Cadastro", type="primary", use_container_width=True):
                    if not cad_nome or not cad_email or not cad_mat or not cad_senha:
                        st.warning("Preencha todos os campos!")
                    elif cad_email.lower().strip() in sistema.alunos_por_email:
                        st.error("Este e-mail já está cadastrado!")
                    elif cad_mat.strip() in sistema.alunos_por_matricula:
                        st.error("Esta matrícula já está cadastrada!")
                    else:
                        try:
                            # Cria o novo aluno e adiciona ao sistema
                            novo_aluno = Aluno(cad_nome.strip(), cad_email.lower().strip(), cad_mat.strip(), cad_senha)
                            sistema.adicionar_aluno(novo_aluno)
                            salvar_sistema_json(sistema)
                            
                            st.success("Conta criada com sucesso! Faça login para entrar.")
                            st.session_state.cadastrando = False
                            st.rerun()
                        except ValueError as e:
                            st.error(f"Erro no cadastro: {e}")
                            
            with col_cad2:
                if st.button("Cancelar", use_container_width=True):
                    st.session_state.cadastrando = False
                    st.rerun()

        # FLUXO 3: TELA DE LOGIN
        else:
            st.subheader("Login")
            email_input = st.text_input("E-mail")
            senha_input = st.text_input("Senha", type="password")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Entrar", type="primary", use_container_width=True):
                    if not email_input or not senha_input:
                        st.warning("Preencha todos os campos!")
                    else:
                        email_chave = email_input.lower().strip()
                        aluno = sistema.alunos_por_email.get(email_chave)
                        
                        if aluno and hasattr(aluno, 'senha') and aluno.senha == senha_input:
                            st.session_state.aluno_logado = aluno
                            st.success("Login efetuado com sucesso!")
                            st.rerun()
                        else:
                            st.error("E-mail ou senha incorretos.")
            
            with col2:
                if st.button("Cadastrar", use_container_width=True):
                    st.session_state.cadastrando = True
                    st.rerun()
                    
            with col3:
                if st.button("Esqueci a senha", use_container_width=True):
                    st.session_state.recuperando_senha = True
                    st.rerun()

# ==========================================================
# SISTEMA PRINCIPAL (APENAS PARA USUÁRIOS LOGADOS)
# ==========================================================
else:
    # SIDEBAR / MENU LATERAL
    with st.sidebar:
        logo_path = ASSETS_DIR / "logo_focusu.png"
        if logo_path.exists():
            st.image(str(logo_path), width=130)

        st.markdown(
            """
            <div style="margin-top: -10px; margin-bottom: 15px;">
                <h3 style="margin: 0; color: white; font-size: 1.2rem; font-weight: 700;">FocusU</h3>
                <p style="margin: 0; color: #71717A; font-size: 0.8rem;">Plataforma Acadêmica</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Mapeamento: (Nome da Tela, Ícone Nativo Material)
        menu_items = [
            ("Home", "home"),
            ("Alunos", "person"),
            ("Disciplinas", "menu_book"),
            ("Agenda", "calendar_today"),
            ("Feed", "forum"),
            ("Estatísticas", "bar_chart"),
        ]

        # Renderiza os botões com ícones integrados
        for nome, icone in menu_items:
            eh_ativa = st.session_state.pagina == nome
            tipo_botao = "primary" if eh_ativa else "secondary"

            if st.button(
                nome,
                key=f"btn_{nome}",
                icon=f":material/{icone}:",
                use_container_width=True,
                type=tipo_botao,
            ):
                st.session_state.pagina = nome
                st.rerun()

        st.divider()
        
        # Área do Usuário
        st.markdown(f"👤 **{st.session_state.aluno_logado.nome}**")
        if st.button("🚪 Sair da Conta", use_container_width=True):
            st.session_state.aluno_logado = None
            st.session_state.pagina = "Home"
            st.rerun()

        st.divider()

        # Botão extra para forçar persistência manual se necessário
        if st.button("💾 Salvar Dados Agora", use_container_width=True):
            if salvar_sistema_json(sistema):
                st.toast("Dados salvos no JSON!", icon="✅")
            else:
                st.toast("Erro ao salvar dados.", icon="❌")

        st.caption("Desenvolvido por Ayra, Bia e Clara")

    # ==========================================================
    # ROTEAMENTO DE TELAS
    # ==========================================================
    pagina_atual = st.session_state.pagina

    if pagina_atual == "Home":
        tela_home(sistema)
    elif pagina_atual == "Alunos":
        tela_alunos(sistema)
    elif pagina_atual == "Disciplinas":
        tela_disciplinas(sistema)
    elif pagina_atual == "Agenda":
        tela_agenda(sistema)
    elif pagina_atual == "Feed":
        tela_feed(sistema)
    elif pagina_atual == "Estatísticas":
        tela_estatisticas(sistema)