import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Importação dos modelos
from models.disciplina import Disciplina
from models.postagem import Postagem, PostagemDuvida, PostagemMaterial
from models.usuario import Aluno
from models.evento import Evento
from utils.helpers import uploaded_file_to_base64

BASE_DIR = Path(__file__).resolve().parent
LOGO = BASE_DIR / "assets" / "logo_focusu.png"


# Helper para conversão de imagem em Base64
def get_image_as_base64(path):
    p = Path(path)
    if not p.exists():
        return ""
    with open(p, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{data}"


ICONS_PATH = {
    "calendar": BASE_DIR / "assets" / "icons" / "calendar.png",
    "chat": BASE_DIR / "assets" / "icons" / "chat.png",
    "livro": BASE_DIR / "assets" / "icons" / "livro.png",
    "rotina": BASE_DIR / "assets" / "icons" / "rotina.png",
    "user": BASE_DIR / "assets" / "icons" / "user.png",
    "dashboard": BASE_DIR / "assets" / "icons" / "dashboard.png",
    "home": BASE_DIR / "assets" / "icons" / "dashboard.png",  # ou use um ícone de home se tiver 
}

ICONS = {key: get_image_as_base64(path) for key, path in ICONS_PATH.items()}


# No topo de paginas.py, adicione esta importação:
from css import carregar_css  # Importa a função do arquivo css.py

# ==========================================================
# 1. TELA HOME
# ==========================================================
def tela_home(sistema):
    # Carrega as imagens em Base64
    logo_simbolo_base64 = get_image_as_base64(LOGO)
    logo_texto_base64 = get_image_as_base64(BASE_DIR / "assets" / "logo.png")

# Banner com a última frase em destaque/legível
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, #161026 0%, #0D0917 100%) !important;
        border: 1px solid #6C5CE7;
        border-radius: 20px;
        padding: 30px;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(108, 92, 231, 0.45);
    ">
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 14px;">
            <img src="{logo_simbolo_base64}" height="50" style="object-fit: contain;">
            <img src="{logo_texto_base64}" height="38" style="object-fit: contain; filter: drop-shadow(0px 2px 5px rgba(255,255,255,0.15));">
        </div>
        <h3 style="color: #A29BFE !important; font-size: 19px; font-weight: 600; margin: 0 0 8px 0; border: none; padding: 0;">
            Plataforma de Organização Universitária
        </h3>
        <p style="color: #E2E2E2 !important; font-size: 14px; margin: 0 0 8px 0;">
            Organize disciplinas, acompanhe sua rotina, publique materiais e compartilhe conhecimento.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.divider()
    # ... segue o restante das métricas e cards ...

    # ... restante do código mantido igual ...

    # Cards Métricas Rápidas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="card">
            <div class="card-icon"><img src="{ICONS['user']}" width="32" height="32" alt="Alunos"></div>
            <div class="card-title">Alunos</div>
            <div class="card-value">{len(sistema.alunos_por_matricula)}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="card">
            <div class="card-icon"><img src="{ICONS['livro']}" width="32" height="32" alt="Disciplinas"></div>
            <div class="card-title">Disciplinas</div>
            <div class="card-value">{len(sistema.disciplinas_por_nome)}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="card">
            <div class="card-icon"><img src="{ICONS['chat']}" width="32" height="32" alt="Postagens"></div>
            <div class="card-title">Postagens</div>
            <div class="card-value">{len(sistema.postagens)}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("## Funcionalidades")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['user']}" width="50" height="50" alt="Alunos"></div>
            <div class="feature-title">Cadastro de Alunos</div>
            <div class="feature-text">Cadastre estudantes e gerencie seus dados acadêmicos.</div>
            <div class="feature-link">➜ Gerenciamento de usuários</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['livro']}" width="50" height="50" alt="Disciplinas"></div>
            <div class="feature-title">Disciplinas</div>
            <div class="feature-text">Gerencie disciplinas, professores e organização do semestre.</div>
            <div class="feature-link">➜ Organização acadêmica</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['chat']}" width="50" height="50" alt="Feed"></div>
            <div class="feature-title">Feed Acadêmico</div>
            <div class="feature-text">Compartilhe materiais, publique dúvidas e interaja com outros alunos.</div>
            <div class="feature-link">➜ Compartilhar conhecimento</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['dashboard']}" width="50" height="50" alt="Dashboard"></div>
            <div class="feature-title">Dashboard</div>
            <div class="feature-text">Visualize indicadores e acompanhe as estatísticas do sistema.</div>
            <div class="feature-link">➜ Visualizar métricas</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Sobre o Projeto")
    st.info("""
    O **FocusU** é uma plataforma desenvolvida para auxiliar estudantes universitários na organização da vida acadêmica.
    O sistema reúne gerenciamento de disciplinas, rotinas, compartilhamento de materiais e interação entre alunos em um único ambiente.
    """)

# ==========================================================
# 2. TELA ALUNOS (Com Upload de Foto)
# ==========================================================
def tela_alunos(sistema):
    st.markdown("<h1>Gerenciamento de Alunos</h1>", unsafe_allow_html=True)
    st.write(
        "Cadastre novos estudantes e gerencie a lista de alunos ativos no sistema."
    )

    col_form, col_lista = st.columns([0.4, 0.6], gap="large")

    # --- COLUNA 1: FORMULÁRIO DE CADASTRO ---
    with col_form:
        st.subheader("➕ Cadastrar Aluno")

        with st.form("cadastro_aluno", clear_on_submit=True):
            nome = st.text_input("Nome Completo", placeholder="Ex: Maria Silva")
            email = st.text_input(
                "E-mail Acadêmico", placeholder="exemplo@universidade.edu.br"
            )
            matricula = st.text_input(
                "Matrícula", placeholder="Ex: 2024100123"
            )

            # Campo para Upload da Foto de Perfil
            foto_upload = st.file_uploader(
                "Foto de Perfil (Opcional)",
                type=["png", "jpg", "jpeg"],
                help="Envie uma foto de perfil do aluno.",
            )

            cadastrar = st.form_submit_button(
                "Cadastrar Aluno", use_container_width=True, type="primary"
            )

        if cadastrar:
            if not nome or not email or not matricula:
                st.warning("⚠️ Preencha todos os campos obrigatórios.")
            else:
                try:
                    # Converte a foto enviada para Base64 (ou None)
                    foto_b64 = uploaded_file_to_base64(foto_upload)

                    aluno = Aluno(nome=nome, email=email, matricula=matricula)

                    # Guarda a imagem base64 no próprio objeto do aluno
                    setattr(aluno, "foto_b64", foto_b64)

                    sistema.adicionar_aluno(aluno)
                    st.success(f"✅ Aluno **{nome}** cadastrado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao cadastrar: {str(e)}")

    # --- COLUNA 2: LISTA DE ALUNOS CADASTRADOS ---
    with col_lista:
        total_alunos = len(sistema.alunos_por_matricula)
        st.subheader(f"👥 Alunos Cadastrados ({total_alunos})")

        if total_alunos > 0:
            termo_busca = st.text_input(
                "🔍 Buscar aluno",
                placeholder="Digite o nome ou matrícula...",
                label_visibility="collapsed",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            alunos_filtrados = [
                a
                for a in sistema.alunos_por_matricula.values()
                if (
                    termo_busca.lower() in a.nome.lower()
                    or termo_busca in a.matricula
                )
            ]

            if not alunos_filtrados:
                st.info("Nenhum aluno encontrado para essa busca.")
            else:
                for aluno in alunos_filtrados:
                    with st.container(border=True):
                        c_avatar, c_info = st.columns([0.22, 0.78])

                        # Pega a foto se existir
                        foto_aluno = getattr(aluno, "foto_b64", None)

                        with c_avatar:
                            if foto_aluno:
                                # Exibe a foto enviada pelo usuário
                                st.markdown(
                                    f"""
                                    <img src="{foto_aluno}" style="
                                        width: 55px; height: 55px; border-radius: 50%;
                                        object-fit: cover; border: 2px solid #6C5CE7;
                                    ">
                                    """,
                                    unsafe_allow_html=True,
                                )
                            else:
                                # Fallback: Avatar com a inicial do nome
                                inicial = (
                                    aluno.nome[0].upper() if aluno.nome else "👤"
                                )
                                st.markdown(
                                    f"""
                                    <div style="
                                        background: linear-gradient(135deg, #6C5CE7, #A29BFE);
                                        width: 55px; height: 55px; border-radius: 50%;
                                        display: flex; align-items: center; justify-content: center;
                                        font-size: 22px; font-weight: bold; color: white;
                                    ">
                                        {inicial}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        with c_info:
                            st.markdown(
                                f"<h4 style='margin:0; color:white;'>{aluno.nome}</h4>",
                                unsafe_allow_html=True,
                            )
                            st.caption(
                                f"📧 {aluno.email}  |  🆔 Matrícula: **{aluno.matricula}**"
                            )

        else:
            st.info("Nenhum aluno cadastrado no momento.")
# ==========================================================
# 3. TELA DISCIPLINAS
# ==========================================================
def tela_disciplinas(sistema):
    st.markdown("<h1>Gerenciamento de Disciplinas</h1>", unsafe_allow_html=True)
    st.write(
        "Cadastre novas disciplinas e visualize as matérias disponíveis na"
        " instituição."
    )

    col_form, col_lista = st.columns([0.4, 0.6], gap="large")

    # --- COLUNA 1: FORMULÁRIO DE CADASTRO ---
    with col_form:
        st.subheader("➕ Cadastrar Disciplina")

        with st.form("cadastro_disciplina", clear_on_submit=True):
            nome = st.text_input(
                "Nome da Disciplina",
                placeholder="Ex: Programação Orientada a Objetos",
            )
            professor = st.text_input(
                "Professor Responsável", placeholder="Ex: Dr. Alan Turing"
            )

            cadastrar = st.form_submit_button(
                "Cadastrar Disciplina", use_container_width=True, type="primary"
            )

        if cadastrar:
            if not nome.strip() or not professor.strip():
                st.warning("⚠️ Preencha o nome da disciplina e o professor.")
            else:
                try:
                    # Instancia a disciplina com nome e professor
                    disciplina = Disciplina(
                        nome=nome.strip(), professor=professor.strip()
                    )

                    # Chama o método exato do seu backend
                    sistema.adicionar_disciplina_global(disciplina)

                    st.success(
                        f"✅ Disciplina **{nome}** cadastrada com sucesso!"
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")

    # --- COLUNA 2: LISTA DE DISCIPLINAS ---
    with col_lista:
        # Pega as disciplinas do dicionário disciplinas_por_nome
        lista_disc = list(sistema.disciplinas_por_nome.values())
        total_disciplinas = len(lista_disc)

        st.subheader(f"📖 Disciplinas Cadastradas ({total_disciplinas})")

        if total_disciplinas > 0:
            termo_busca = st.text_input(
                "🔍 Buscar disciplina",
                placeholder="Digite o nome da disciplina ou do professor...",
                label_visibility="collapsed",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            disciplinas_filtradas = [
                d
                for d in lista_disc
                if (
                    termo_busca.lower() in d.nome.lower()
                    or termo_busca.lower() in d.professor.lower()
                )
            ]

            if not disciplinas_filtradas:
                st.info("Nenhuma disciplina encontrada para essa busca.")
            else:
                for disc in disciplinas_filtradas:
                    with st.container(border=True):
                        st.markdown(
                            f"<h4 style='margin:0; color:white;'>{disc.nome}</h4>",
                            unsafe_allow_html=True,
                        )
                        st.caption(
                            f"👨‍🏫 **Professor Responsável:** {disc.professor}"
                        )

        else:
            st.info("Nenhuma disciplina cadastrada no momento.")
# ==========================================================
# 4. TELA FEED (ESTILO INSTAGRAM FIEL Á IMAGEM)
# ==========================================================
def tela_feed(sistema):
    st.markdown("<h1>Feed da Comunidade</h1>", unsafe_allow_html=True)

    tab_feed, tab_novo = st.tabs(["📸 Feed", "➕ Nova Publicação"])

    alunos_disponiveis = list(sistema.alunos_por_matricula.values())

    # ------------------------------------------------------
    # ABA 1: FEED IGUAL AO INSTAGRAM
    # ------------------------------------------------------
    with tab_feed:
        feed_items = sistema.postagens + sistema.eventos

        if not feed_items:
            st.info("Nenhuma publicação no momento.")
        else:
            _, col_central, _ = st.columns([0.15, 0.7, 0.15])

            with col_central:
                for idx, item in enumerate(reversed(feed_items)):
                    is_evento = isinstance(item, Evento) or hasattr(
                        item, "horario"
                    )

                    autor_obj = getattr(item, "autor", None)
                    nome_autor = getattr(
                        autor_obj,
                        "nome",
                        "clara" if autor_obj else "Institucional",
                    )
                    foto_autor = getattr(autor_obj, "foto_b64", None)
                    foto_post = getattr(item, "foto_post_b64", None)

                    # Avatar do Autor
                    if foto_autor:
                        avatar_html = f'<img src="{foto_autor}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">'
                    else:
                        letra = nome_autor[0].upper() if nome_autor else "U"
                        avatar_html = f"""
                        <div style="
                            background: linear-gradient(135deg, #C13584, #E1306C, #FD1D1D);
                            width: 32px; height: 32px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: bold; font-size: 14px;
                        ">{letra}</div>
                        """

                    # CARD DO POST
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #121214;
                            border: 1px solid #27272A;
                            border-radius: 10px;
                            margin-bottom: 28px;
                            padding-bottom: 12px;
                        ">
                            <!-- HEADER DO POST -->
                            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 14px;">
                                {avatar_html}
                                <span style="color: white; font-weight: 600; font-size: 14px;">{nome_autor.lower()}</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # FOTO DO POST (Sem cortar)
                    if foto_post:
                        st.markdown(
                            f"""
                            <div style="width: 100%; background: #000; text-align: center;">
                                <img src="{foto_post}" style="width: 100%; max-height: 600px; object-fit: contain;">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    # ÁREA DE CONTEÚDO E LEGENDA (Estilo Instagram)
                    st.markdown(
                        '<div style="padding: 10px 14px 0px 14px;">',
                        unsafe_allow_html=True,
                    )

                    if hasattr(item, "titulo") and item.titulo:
                        st.markdown(
                            f"<h4 style='color: white; margin: 0 0 4px"
                            f" 0;'>{item.titulo}</h4>",
                            unsafe_allow_html=True,
                        )

                    conteudo_texto = getattr(item, "conteudo", "")
                    if conteudo_texto:
                        st.markdown(
                            f"<p style='color: #E4E4E7; font-size: 14px;"
                            f" margin: 0;'><strong"
                            f" style='color:white;'>{nome_autor.lower()}</strong>"
                            f" {conteudo_texto}</p>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

                    # BOTÃO CURTIR
                    if not is_evento and hasattr(item, "curtir"):
                        st.markdown(
                            '<div style="padding: 6px 14px;">',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"❤️ {item.curtidas} curtidas", key=f"like_{idx}"
                        ):
                            item.curtir()
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    # LISTA DE COMENTÁRIOS (Igual à imagem que você mandou)
                    if not is_evento and hasattr(item, "comentarios"):
                        st.markdown(
                            '<div style="padding: 0px 14px;">',
                            unsafe_allow_html=True,
                        )

                        if item.comentarios:
                            for c in item.comentarios:
                                # Trata se o comentário tiver autor ou for texto puro
                                if "::" in str(c):
                                    c_autor, c_texto = str(c).split("::", 1)
                                else:
                                    c_autor, c_texto = (
                                        nome_autor.lower(),
                                        str(c),
                                    )

                                st.markdown(
                                    f"""
                                    <div style="display: flex; align-items: flex-start; gap: 8px; margin-top: 8px;">
                                        <div style="background: #3F3F46; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 11px; font-weight: bold;">
                                            {c_autor[0].upper()}
                                        </div>
                                        <div>
                                            <span style="color: white; font-weight: 600; font-size: 13px;">{c_autor.lower()}</span>
                                            <span style="color: #D4D4D8; font-size: 13px; margin-left: 4px;">{c_texto}</span>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        st.markdown("</div>", unsafe_allow_html=True)

                        # FORMULÁRIO DE COMENTAR
                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.form(
                            key=f"form_coment_{idx}", clear_on_submit=True
                        ):
                            c_user, c_input, c_btn = st.columns([0.3, 0.55, 0.15])

                            with c_user:
                                comentador = st.selectbox(
                                    "Quem comenta",
                                    options=alunos_disponiveis
                                    if alunos_disponiveis
                                    else ["Usuário"],
                                    format_func=lambda a: a.nome
                                    if hasattr(a, "nome")
                                    else str(a),
                                    label_visibility="collapsed",
                                    key=f"sel_{idx}",
                                )

                            with c_input:
                                txt_coment = st.text_input(
                                    "Adicionar comentário...",
                                    placeholder="Adicionar comentário...",
                                    label_visibility="collapsed",
                                    key=f"in_{idx}",
                                )

                            with c_btn:
                                if st.form_submit_button("Publicar"):
                                    if txt_coment.strip():
                                        autor_nome_c = (
                                            comentador.nome
                                            if hasattr(comentador, "nome")
                                            else "Usuário"
                                        )
                                        # Salva no formato Autor::Texto
                                        item.comentar(
                                            f"{autor_nome_c}::{txt_coment.strip()}"
                                        )
                                        st.rerun()

                    # Fecha a div do Card
                    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # ABA 2: CRIAR PUBLICAÇÃO
    # ------------------------------------------------------
    with tab_novo:
        st.subheader("O que você deseja compartilhar?")

        categoria = st.radio(
            "Tipo de Publicação",
            ["Post Geral", "Dúvida", "Material", "Evento"],
            horizontal=True,
        )

        if not alunos_disponiveis and categoria != "Evento":
            st.warning(
                "⚠️ Cadastre pelo menos um aluno na aba 'Alunos' antes de criar"
                " uma postagem."
            )
        else:
            with st.form("form_nova_pub", clear_on_submit=True):
                if categoria != "Evento":
                    aluno_selecionado = st.selectbox(
                        "Autor da Publicação",
                        options=alunos_disponiveis,
                        format_func=lambda a: f"{a.nome} ({a.matricula})",
                    )
                    titulo = st.text_input(
                        "Título", placeholder="Ex: Foto no campus"
                    )
                    conteudo = st.text_area(
                        "Legenda", placeholder="Escreva a legenda..."
                    )

                    foto_post_upload = st.file_uploader(
                        "Anexar Foto", type=["png", "jpg", "jpeg"]
                    )

                    disciplina_nome = ""
                    link_download = ""
                    if categoria == "Dúvida":
                        disciplina_nome = st.text_input("Nome da Disciplina")
                    elif categoria == "Material":
                        link_download = st.text_input("Link do Material")

                    submeter = st.form_submit_button(
                        "Publicar no Feed",
                        use_container_width=True,
                        type="primary",
                    )

                    if submeter:
                        if not titulo.strip() or not conteudo.strip():
                            st.warning("⚠️ Preencha o título e a legenda.")
                        else:
                            try:
                                foto_b64 = uploaded_file_to_base64(
                                    foto_post_upload
                                )

                                if categoria == "Post Geral":
                                    post = Postagem(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_selecionado,
                                    )
                                elif categoria == "Dúvida":
                                    post = PostagemDuvida(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_selecionado,
                                        disciplina=disciplina_nome.strip()
                                        or "Geral",
                                    )
                                else:
                                    post = PostagemMaterial(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_selecionado,
                                        link_download=link_download.strip()
                                        or "#",
                                    )

                                setattr(post, "foto_post_b64", foto_b64)
                                sistema.adicionar_postagem(post)
                                st.success("✅ Publicado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao publicar: {str(e)}")

                else:  # Criar Evento
                    titulo_ev = st.text_input(
                        "Título do Evento", placeholder="Ex: Hackathon FocusU"
                    )
                    c_data, c_hora = st.columns(2)
                    with c_data:
                        data_ev = st.date_input("Data do Evento")
                    with c_hora:
                        horario_ev = st.time_input("Horário do Evento")

                    submeter = st.form_submit_button(
                        "Criar Evento", use_container_width=True, type="primary"
                    )

                    if submeter:
                        if not titulo_ev.strip():
                            st.warning("⚠️ O título não pode ser vazio.")
                        else:
                            try:
                                evento = Evento(
                                    titulo=titulo_ev.strip(),
                                    data=data_ev.strftime("%d/%m/%Y"),
                                    horario=horario_ev.strftime("%H:%M"),
                                )
                                sistema.adicionar_evento(evento)
                                st.success("✅ Evento criado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao criar evento: {str(e)}")
# ==========================================================
# 5. TELA ESTATÍSTICAS
# ==========================================================
import pandas as pd


# ==========================================================
# 5. TELA DE ESTATÍSTICAS E DASHBOARD
# ==========================================================
def tela_estatisticas(sistema):
    st.markdown(
        "<h1>📊 Dashboard de Estatísticas</h1>", unsafe_allow_html=True
    )
    st.write(
        "Acompanhe o engajamento da comunidade e as métricas do FocusU em tempo"
        " real."
    )

    # Coleta de Dados do Sistema
    alunos = list(sistema.alunos_por_matricula.values())
    postagens = sistema.postagens
    eventos = sistema.eventos

    total_alunos = len(alunos)
    total_posts = len(postagens)
    total_eventos = len(eventos)

    # Cálculo de métricas
    total_curtidas = sum(getattr(p, "curtidas", 0) for p in postagens)
    total_comentarios = sum(
        len(getattr(p, "comentarios", [])) for p in postagens
    )

    # ------------------------------------------------------
    # 1. CARDS DE MÉTRICAS (KPIs)
    # ------------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("👥 Alunos", total_alunos)
    with c2:
        st.metric("📝 Posts", total_posts)
    with c3:
        st.metric("❤️ Curtidas", total_curtidas)
    with c4:
        st.metric("💬 Comentários", total_comentarios)
    with c5:
        st.metric("📅 Eventos", total_eventos)

    st.markdown("---")

    if not postagens and not eventos:
        st.info(
            "💡 Ainda não há publicações ou eventos suficientes para gerar"
            " gráficos. Crie posts na aba Feed para visualizar as métricas!"
        )
        return

    # ------------------------------------------------------
    # 2. GRÁFICOS E RANKINGS
    # ------------------------------------------------------
    col_left, col_right = st.columns(2)

    # --- Gráfico de Tipos de Postagem ---
    with col_left:
        st.subheader("📌 Distribuição de Conteúdo")

        qtd_duvidas = sum(
            1 for p in postagens if isinstance(p, PostagemDuvida)
        )
        qtd_materiais = sum(
            1 for p in postagens if isinstance(p, PostagemMaterial)
        )
        qtd_geral = total_posts - (qtd_duvidas + qtd_materiais)

        dados_tipos = {
            "Tipo": ["Geral", "Dúvidas", "Materiais", "Eventos"],
            "Quantidade": [qtd_geral, qtd_duvidas, qtd_materiais, total_eventos],
        }

        df_tipos = pd.DataFrame(dados_tipos)
        st.bar_chart(df_tipos.set_index("Tipo"))

    # --- Ranking de Alunos Mais Ativos ---
    with col_right:
        st.subheader("🏆 Ranking de Autores (Posts)")

        contagem_autores = {}
        for p in postagens:
            autor = getattr(p, "autor", None)
            nome = getattr(autor, "nome", "Institucional")
            contagem_autores[nome] = contagem_autores.get(nome, 0) + 1

        if contagem_autores:
            df_autores = pd.DataFrame(
                list(contagem_autores.items()),
                columns=["Aluno / Autor", "Publicações"],
            )
            df_autores = df_autores.sort_values(
                by="Publicações", ascending=False
            ).head(5)

            st.dataframe(
                df_autores,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.caption("Sem dados de autores suficientes.")

    # ------------------------------------------------------
    # 3. DESTAQUES DA COMUNIDADE
    # ------------------------------------------------------
    st.markdown("---")
    st.subheader("⭐ Publicação em Destaque")

    if postagens:
        top_post = max(postagens, key=lambda p: getattr(p, "curtidas", 0))
        curtidas_top = getattr(top_post, "curtidas", 0)

        if curtidas_top > 0:
            autor_obj = getattr(top_post, "autor", None)
            nome_autor = getattr(
                autor_obj,
                "nome",
                "clara" if autor_obj else "Institucional",
            )

            st.success(
                f"🔥 **Post Mais Curtido:** '{top_post.titulo}' por"
                f" **@{nome_autor.lower()}** com **{curtidas_top} curtidas** e"
                f" **{len(getattr(top_post, 'comentarios', []))} comentários**!"
            )
        else:
            st.info(
                "Nenhuma publicação recebeu curtidas ainda. Seja o primeiro a"
                " interagir no Feed!"
            )

# ==========================================================
# ESTRUTURA PRINCIPAL E NAVEGAÇÃO
# ==========================================================
def main(sistema):
    carregar_css()

    # Guarda a página atual no session_state
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Home"

    with st.sidebar:
        # Cabeçalho da Sidebar
        if LOGO.exists():
            st.image(str(LOGO), width=110)

        st.markdown(
            """
        <div style="margin-top:-5px; margin-bottom:20px;">
            <h3 style="margin:0; color:white; font-size:1.1rem; font-weight:700;">FocusU</h3>
            <p style="margin:0; color:#71717A; font-size:0.8rem;">Plataforma Acadêmica</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Mapeamento dos botões da sidebar
        botoes = [
            ("Home", "home"),
            ("Alunos", "user"),
            ("Disciplinas", "livro"),
            ("Feed", "chat"),
            ("Estatísticas", "dashboard"),
        ]

        # Criar os botões verticais na Sidebar
        for nome, chave_icone in botoes:
            eh_ativa = st.session_state.pagina == nome
            tipo_botao = "primary" if eh_ativa else "secondary"
            
            # Pega o ícone base64 correspondente
            img_icon = ICONS.get(chave_icone, "")

            # Exibe o ícone e o botão em colunas para ficarem lado a lado
            col_icon, col_btn = st.columns([0.2, 0.8])
            
            with col_icon:
                if img_icon:
                    st.markdown(
                        f'<img src="{img_icon}" width="22" style="margin-top: 8px;">',
                        unsafe_allow_html=True
                    )
            
            with col_btn:
                if st.button(
                    nome,
                    key=f"nav_btn_{nome}",
                    use_container_width=True,
                    type=tipo_botao,
                ):
                    st.session_state.pagina = nome
                    st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("Versão 1.0")

    # Direcionamento das telas
    opcao = st.session_state.pagina

    if opcao == "Home":
        tela_home(sistema)
    elif opcao == "Alunos":
        tela_alunos(sistema)
    elif opcao == "Disciplinas":
        tela_disciplinas(sistema)
    elif opcao == "Feed":
        tela_feed(sistema)
    elif opcao == "Estatísticas":
        tela_estatisticas(sistema)