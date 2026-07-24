from pathlib import Path
import sys

# ==========================================================
# AJUSTE DE CAMINHOS PARA O STREAMLIT CLOUD (RAIZ DO PROJETO)
# ==========================================================
WEB_DIR = Path(__file__).resolve().parent
SRC_DIR = WEB_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

# Adiciona a raiz do projeto e a pasta src ao sys.path
for caminho in [str(PROJECT_ROOT), str(SRC_DIR), str(WEB_DIR)]:
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

import streamlit as st
from css import carregar_css
from paginas import (
    tela_alunos,
    tela_disciplinas,
    tela_estatisticas,
    tela_feed,
    tela_home,
)
from system.sistema import SistemaFocusU

# Configuração da página
st.set_page_config(page_title="FocusU", page_icon="🎓", layout="wide")

# Aplica o CSS
st.markdown(carregar_css(), unsafe_allow_html=True)

# Inicializa o Sistema no state
if "sistema" not in st.session_state:
    st.session_state.sistema = SistemaFocusU()

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
elif pagina_atual == "Feed":
    tela_feed(sistema)
elif pagina_atual == "Estatísticas":
    tela_estatisticas(sistema)