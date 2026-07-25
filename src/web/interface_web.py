from pathlib import Path
import sys

WEB_DIR = Path(__file__).resolve().parent
SRC_DIR = WEB_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

for c in [str(PROJECT_ROOT), str(SRC_DIR), str(WEB_DIR)]:
    if c not in sys.path:
        sys.path.insert(0, c)

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

# CRUCIAL: Importa as funções de carregar/salvar JSON
# (Caso o arquivo com as funções do JSON esteja em outro caminho, ajuste esta linha)
try:
    from src.system.banco import carregar_sistema_json, salvar_sistema_json
except ImportError:
    try:
        from banco import carregar_sistema_json, salvar_sistema_json
    except ImportError:
        from src.banco import carregar_sistema_json, salvar_sistema_json

# Configuração da página
st.set_page_config(page_title="FocusU", page_icon="🎓", layout="wide")

# Aplica o CSS
st.markdown(carregar_css(), unsafe_allow_html=True)

# ==========================================================
# INICIALIZAÇÃO E CARREGAMENTO DO BANCO DE DADOS (JSON)
# ==========================================================
if "sistema" not in st.session_state:
    # 1. Instancia a classe principal
    instancia_sistema = SistemaFocusU()
    # 2. POPULA o sistema com os dados salvos do JSON antes de colocar na sessão!
    st.session_state.sistema = carregar_sistema_json(instancia_sistema)

# Guarda a página atual no state
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

sistema = st.session_state.sistema
ASSETS_DIR = WEB_DIR / "assets"

# ==========================================================
# SIDEBAR / MENU LATERAL
# ==========================================================
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