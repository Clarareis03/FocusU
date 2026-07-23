import streamlit as st

from css import carregar_css

from paginas import (
    tela_home,
    tela_alunos,
    tela_disciplinas,
    tela_feed,
    tela_estatisticas
)

from system.sistema import SistemaFocusU

st.set_page_config(

    page_title="FocusU",

    page_icon="🎓",

    layout="wide"

)

st.markdown(
    carregar_css(),
    unsafe_allow_html=True
)

if "sistema" not in st.session_state:

    st.session_state.sistema = SistemaFocusU()

sistema = st.session_state.sistema

pagina = st.sidebar.radio(

    "MENU",

    [

        "🏠 Home",

        "👤 Alunos",

        "📚 Disciplinas",

        "📝 Feed",

        "📊 Estatísticas"

    ]

)

if pagina=="🏠 Home":

    tela_home(sistema)

elif pagina=="👤 Alunos":

    tela_alunos(sistema)

elif pagina=="📚 Disciplinas":

    tela_disciplinas(sistema)

elif pagina=="📝 Feed":

    tela_feed(sistema)

else:

    tela_estatisticas(sistema)

