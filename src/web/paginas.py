
import base64
import uuid
from datetime import datetime, date
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
from css import carregar_css  # Importa a função do arquivo css.py
from utils.persistencia import salvar_sistema_json

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
    "home": BASE_DIR / "assets" / "icons" / "dashboard.png",
}

ICONS = {key: get_image_as_base64(path) for key, path in ICONS_PATH.items()}


# ==========================================================
# 1. TELA HOME
# ==========================================================
def tela_home(sistema):
    logo_simbolo_base64 = get_image_as_base64(LOGO)
    logo_texto_base64 = get_image_as_base64(BASE_DIR / "assets" / "logo.png")

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
    
    # ------------------ LINHA 1 ------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['user']}" width="50" height="50" alt="Alunos"></div>
            <div class="feature-title">Cadastro de Alunos</div>
            <div class="feature-text">Cadastre estudantes e gerencie seus dados acadêmicos.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("➜ Gerenciamento de usuários", key="card_btn_alunos"):
            st.session_state.pagina = "Alunos"
            st.rerun()

    with col2:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['livro']}" width="50" height="50" alt="Disciplinas"></div>
            <div class="feature-title">Disciplinas</div>
            <div class="feature-text">Gerencie disciplinas, professores e organização do semestre.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("➜ Organização acadêmica", key="card_btn_disciplinas"):
            st.session_state.pagina = "Disciplinas"
            st.rerun()

    # ------------------ LINHA 2 ------------------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['chat']}" width="50" height="50" alt="Feed"></div>
            <div class="feature-title">Feed Acadêmico</div>
            <div class="feature-text">Compartilhe materiais, publique dúvidas e interaja com outros alunos.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("➜ Compartilhar conhecimento", key="card_btn_feed"):
            st.session_state.pagina = "Feed"
            st.rerun()

    with col4:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon"><img src="{ICONS['dashboard']}" width="50" height="50" alt="Dashboard"></div>
            <div class="feature-title">Dashboard</div>
            <div class="feature-text">Visualize indicadores e acompanhe as estatísticas do sistema.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("➜ Visualizar métricas", key="card_btn_estatisticas"):
            st.session_state.pagina = "Estatísticas"
            st.rerun()

    st.divider()

    st.subheader("Sobre o Projeto")
    st.info("""
    O **FocusU** é uma plataforma desenvolvida para auxiliar estudantes universitários na organização da vida acadêmica.
    O sistema reúne gerenciamento de disciplinas, rotinas, compartilhamento de materiais e interação entre alunos em um único ambiente.
    """)
# ==========================================================
# 2. TELA ALUNOS (LOGIN & SESSÃO ÚNICA)
# ==========================================================
def tela_alunos(sistema):
    st.markdown("<h1>Meu Perfil & Sessão</h1>", unsafe_allow_html=True)

    # Recupera o aluno logado na sessão ativa
    aluno_logado = st.session_state.get("aluno_logado", None)

    # ==========================================================
    # CASO 1: ALUNO LOGADO NA SESSÃO
    # ==========================================================
    if aluno_logado:
        col_tit, col_logout = st.columns([0.7, 0.3])
        with col_tit:
            st.write("Gerencie seu perfil acadêmico e acompanhe seu progresso.")
        with col_logout:
            if st.button("🚪 Sair da Conta", use_container_width=True):
                st.session_state["aluno_logado"] = None
                st.rerun()

        # Carteirinha do Aluno
        with st.container(border=True):
            col_avatar_p, col_info_p = st.columns([0.25, 0.75])

            foto_aluno_p = getattr(aluno_logado, "foto_b64", None)

            with col_avatar_p:
                if foto_aluno_p:
                    st.markdown(
                        f"""
                        <img src="{foto_aluno_p}" style="
                            width: 90px; height: 90px; border-radius: 50%;
                            object-fit: cover; border: 3px solid #6C5CE7;
                        ">
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    inicial_p = (
                        aluno_logado.nome[0].upper() if aluno_logado.nome else "👤"
                    )
                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(135deg, #6C5CE7, #A29BFE);
                            width: 90px; height: 90px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center;
                            font-size: 36px; font-weight: bold; color: white;
                        ">
                            {inicial_p}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with col_info_p:
                st.markdown(f"<h3 style='margin:0; color:white;'>{aluno_logado.nome}</h3>", unsafe_allow_html=True)
                st.caption(f"📧 {aluno_logado.email}  |  🆔 Matrícula: **{aluno_logado.matricula}**")

                minutos_estudo = aluno_logado.calcular_tempo_estudo_recursivo()
                horas = minutos_estudo // 60
                mins = minutos_estudo % 60
                st.markdown(f"⏱️ **Tempo Total Dedicado:** `{horas}h {mins}min`")

        # Progresso + Tarefas Pendentes
        col_prog, col_pend = st.columns(2)

        with col_prog:
            st.markdown("##### 📊 Progresso Acadêmico")
            progresso = aluno_logado.calcular_progresso_estudos(sistema)
            st.progress(progresso / 100.0)
            st.caption(f"**{progresso}%** das atividades do sistema foram concluídas!")

        with col_pend:
            st.markdown("##### 📌 Tarefas Pendentes")
            tarefas_pendentes = aluno_logado.obter_tarefas_pendentes(sistema)
            if tarefas_pendentes:
                for t in tarefas_pendentes[:2]:
                    st.warning(f"**{t['titulo']}** ({t['disciplina']}) — Entrega: `{t['data_entrega']}`")
            else:
                st.success("Nenhuma tarefa pendente no momento! 🎉")

        st.divider()

        # Editar Perfil
        with st.expander("✏️ Editar Meu Perfil"):
            with st.form("form_editar_perfil"):
                novo_nome = st.text_input("Novo Nome", value=aluno_logado.nome)
                novo_email = st.text_input("Novo E-mail", value=aluno_logado.email)
                nova_foto = st.file_uploader("Trocar Foto", type=["png", "jpg", "jpeg"])

                if st.form_submit_button("Salvar Alterações", type="primary"):
                    try:
                        b64_foto = None
                        if nova_foto:
                            b64_foto = uploaded_file_to_base64(nova_foto)

                        aluno_logado.atualizar_perfil(novo_nome, novo_email, b64_foto)
                        salvar_sistema_json(sistema)

                        st.success("✅ Perfil atualizado com sucesso!")
                        st.rerun()
                    except Exception as err:
                        st.error(f"❌ Erro ao atualizar: {err}")

    # ==========================================================
    # CASO 2: SEM SESSÃO ATIVA (LOGIN OU REGISTRO)
    # ==========================================================
    else:
        st.info("👋 Faça login com sua matrícula e senha ou crie uma conta para acessar o sistema.")

        tab_login, tab_cadastrar = st.tabs(["🔑 Entrar", "➕ Criar Conta"])

        # --- ABA LOGIN ---
        with tab_login:
            st.subheader("Acessar Conta")
            with st.form("form_login"):
                matricula_login = st.text_input("Matrícula", placeholder="Digite sua matrícula")
                senha_login = st.text_input("Senha", type="password", placeholder="Digite sua senha")

                entrar = st.form_submit_button("Entrar", type="primary", use_container_width=True)

            if entrar:
                if not matricula_login or not senha_login:
                    st.warning("⚠️ Preencha a matrícula e a senha.")
                else:
                    # Busca o aluno no dicionário de matrículas
                    aluno_encontrado = sistema.alunos_por_matricula.get(matricula_login.strip())
                    
                    # Verifica a senha (usando atributo `senha` do objeto Aluno)
                    senha_salva = getattr(aluno_encontrado, "senha", None) if aluno_encontrado else None

                    if aluno_encontrado and senha_salva == senha_login:
                        st.session_state["aluno_logado"] = aluno_encontrado
                        st.success(f"✅ Bem-vindo(a) de volta, {aluno_encontrado.nome}!")
                        st.rerun()
                    else:
                        st.error("❌ Matrícula ou senha incorretas.")

        # --- ABA CADASTRO ---
        with tab_cadastrar:
            st.subheader("Criar Nova Conta")
            with st.form("form_cadastro", clear_on_submit=True):
                nome = st.text_input("Nome Completo", placeholder="Ex: Maria Silva")
                email = st.text_input("E-mail Acadêmico", placeholder="exemplo@universidade.edu.br")
                matricula = st.text_input("Matrícula", placeholder="Ex: 2024100123")
                senha = st.text_input("Senha", type="password", placeholder="Crie uma senha de acesso")

                foto_upload = st.file_uploader("Foto de Perfil (Opcional)", type=["png", "jpg", "jpeg"])

                cadastrar = st.form_submit_button("Cadastrar e Entrar", use_container_width=True, type="primary")

            if cadastrar:
                if not nome or not email or not matricula or not senha:
                    st.warning("⚠️ Preencha todos os campos obrigatórios (incluindo a senha).")
                elif matricula.strip() in sistema.alunos_por_matricula:
                    st.error("❌ Esta matrícula já está cadastrada no sistema.")
                else:
                    try:
                        foto_b64 = uploaded_file_to_base64(foto_upload) if foto_upload else None
                        
                        aluno = Aluno(nome=nome.strip(), email=email.strip(), matricula=matricula.strip())
                        
                        # Atribui a senha e a foto ao objeto
                        setattr(aluno, "senha", senha)
                        if foto_b64:
                            setattr(aluno, "foto_b64", foto_b64)

                        # Salva no sistema e no JSON
                        sistema.adicionar_aluno(aluno)
                        salvar_sistema_json(sistema)

                        # Inicia sessão diretamente
                        st.session_state["aluno_logado"] = aluno

                        st.success(f"✅ Conta criada com sucesso! Bem-vindo(a), {nome}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar: {str(e)}")

# ==========================================================
# 3. TELA DISCIPLINAS
# ==========================================================
def tela_disciplinas(sistema):
    st.markdown("<h1>Gerenciamento de Disciplinas</h1>", unsafe_allow_html=True)
    st.write(
        "Cadastre novas disciplinas e visualize as matérias disponíveis na instituição."
    )

    col_form, col_lista = st.columns([0.4, 0.6], gap="large")

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
                    disciplina = Disciplina(
                        nome=nome.strip(), professor=professor.strip()
                    )
                    sistema.adicionar_disciplina_global(disciplina)

                    # 🟢 SALVA NO BANCO DE DADOS (JSON)
                    salvar_sistema_json(sistema)

                    st.success(
                        f"✅ Disciplina **{nome}** cadastrada com sucesso!"
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")
    with col_lista:
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
# 4. TELA AGENDA (Atualizada com OO)
# ==========================================================
def tela_agenda(sistema):
    st.markdown("<h1>📅 Agenda de Tarefas</h1>", unsafe_allow_html=True)
    st.write("Acompanhe suas provas, entregas e trabalhos organizados por disciplina.")

    dict_disciplinas = sistema.disciplinas_por_nome

    if not dict_disciplinas:
        st.warning("⚠️ Cadastre pelo menos uma disciplina na aba 'Disciplinas' para utilizar a agenda.")
        return

    col_filtro, _ = st.columns([0.4, 0.6])
    with col_filtro:
        filtro_status = st.radio(
            "Filtrar por status:",
            options=["Todas", "Pendentes", "Concluídas"],
            horizontal=True
        )

    st.divider()

    with st.expander("➕ Cadastrar Nova Tarefa"):
        with st.form("form_nova_tarefa", clear_on_submit=True):
            col_disc, col_tipo = st.columns(2)

            with col_disc:
                nome_disc_selecionada = st.selectbox("Disciplina", list(dict_disciplinas.keys()))
            with col_tipo:
                tipo = st.selectbox("Tipo", ["Prova", "Entrega", "Trabalho", "Lista"])

            col_titulo, col_data = st.columns([0.6, 0.4])
            with col_titulo:
                titulo = st.text_input("Título da Tarefa", placeholder="Ex: P1 de Cálculo, Trabalho em Grupo...")
            with col_data:
                data_entrega = st.date_input("Data de Entrega", min_value=date.today())

            descricao = st.text_area("Descrição (opcional)", placeholder="Detalhes adicionais ou links úteis...")

            cadastrar = st.form_submit_button("Salvar Tarefa", type="primary", use_container_width=True)

            if cadastrar:
                if not titulo.strip():
                    st.error("⚠️ O título da tarefa é obrigatório!")
                else:
                    disciplina_obj = dict_disciplinas[nome_disc_selecionada]
                    tarefa_criada = disciplina_obj.adicionar_tarefa(
                        titulo=titulo.strip(),
                        data_entrega=data_entrega,
                        tipo=tipo,
                        descricao=descricao.strip()
                    )

                    #  SALVA NO BANCO DE DADOS (JSON)
                    salvar_sistema_json(sistema)

                    st.success(f"✅ Tarefa **'{tarefa_criada.titulo}'** adicionada à disciplina **{nome_disc_selecionada}**!")
                    st.rerun()

    st.markdown("### 📚 Tarefas por Disciplina")

    icones_tipo = {
        "Prova": "📝",
        "Entrega": "📦",
        "Trabalho": "👥",
        "Lista": "📄"
    }

    status_param = None
    if filtro_status == "Pendentes":
        status_param = "pendentes"
    elif filtro_status == "Concluídas":
        status_param = "concluidas"

    for nome_disc, disciplina_obj in dict_disciplinas.items():
        tarefas_brutas = disciplina_obj.listar_tarefas(status=status_param)

        # FILTRAGEM DE SEGURANÇA NA INTERFACE:
        # Garante que apenas tarefas do status selecionado serão exibidas
        if filtro_status == "Pendentes":
            tarefas = [t for t in tarefas_brutas if not getattr(t, "concluida", False)]
        elif filtro_status == "Concluídas":
            tarefas = [t for t in tarefas_brutas if getattr(t, "concluida", False)]
        else:
            tarefas = tarefas_brutas

        with st.expander(f"📖 **{nome_disc}** ({len(tarefas)} tarefas)", expanded=True):
            if not tarefas:
                st.caption("Nenhuma tarefa encontrada para os filtros selecionados.")
                continue

            for tarefa in tarefas:
                col_check, col_info = st.columns([0.08, 0.92])

                with col_check:
                    ja_concluida = getattr(tarefa, "concluida", False)
                    marcado = st.checkbox(
                        label="Concluir",
                        value=ja_concluida,
                        key=f"chk_{tarefa.id}",
                        label_visibility="collapsed"
                    )

                    if marcado != ja_concluida:
                        if marcado:
                            if hasattr(disciplina_obj, "concluir_tarefa"):
                                disciplina_obj.concluir_tarefa(tarefa.id)
                            else:
                                tarefa.concluida = True
                        else:
                            tarefa.concluida = False

                        #  SALVA NO BANCO DE DADOS (JSON)
                        salvar_sistema_json(sistema)

                        st.rerun()

                with col_info:
                    icone = icones_tipo.get(tarefa.tipo, "📌")
                    data_str = tarefa.data_entrega.strftime("%d/%m/%Y") if hasattr(tarefa.data_entrega, "strftime") else str(tarefa.data_entrega)

                    if tarefa.concluida:
                        st.markdown(f"~~{icone} **[{tarefa.tipo}]** {tarefa.titulo} — *Vencimento: {data_str}*~~")
                    else:
                        st.markdown(f"{icone} **[{tarefa.tipo}]** **{tarefa.titulo}** — 🗓️ *Vencimento: {data_str}*")

                    if tarefa.descricao:
                        st.caption(f"💬 {tarefa.descricao}")

                    if not tarefa.concluida and isinstance(tarefa.data_entrega, date) and tarefa.data_entrega < date.today():
                        st.warning("⚠️ Esta tarefa está em atraso!")

                st.divider()

# ==========================================================
# 5. TELA FEED (INTEGRADA COM ALUNO LOGADO)
# ==========================================================
def tela_feed(sistema):
    st.markdown("<h1>Feed da Comunidade</h1>", unsafe_allow_html=True)

    tab_feed, tab_novo = st.tabs(["📸 Feed", "➕ Nova Publicação"])

    # Recupera o aluno logado na sessão
    aluno_logado = st.session_state.get("aluno_logado", None)

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

                    st.markdown(
                        f"""
                        <div style="
                            background-color: #121214;
                            border: 1px solid #27272A;
                            border-radius: 10px;
                            margin-bottom: 28px;
                            padding-bottom: 12px;
                        ">
                            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 14px;">
                                {avatar_html}
                                <span style="color: white; font-weight: 600; font-size: 14px;">{nome_autor.lower()}</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if foto_post:
                        st.markdown(
                            f"""
                            <div style="width: 100%; background: #000; text-align: center;">
                                <img src="{foto_post}" style="width: 100%; max-height: 600px; object-fit: contain;">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        '<div style="padding: 10px 14px 0px 14px;">',
                        unsafe_allow_html=True,
                    )

                    if hasattr(item, "titulo") and item.titulo:
                        st.markdown(
                            f"<h4 style='color: white; margin: 0 0 4px 0;'>{item.titulo}</h4>",
                            unsafe_allow_html=True,
                        )

                    conteudo_texto = getattr(item, "conteudo", "")
                    if conteudo_texto:
                        st.markdown(
                            f"<p style='color: #E4E4E7; font-size: 14px; margin: 0;'><strong style='color:white;'>{nome_autor.lower()}</strong> {conteudo_texto}</p>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

                    if not is_evento and hasattr(item, "curtir"):
                        st.markdown(
                            '<div style="padding: 6px 14px;">',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"❤️ {item.curtidas} curtidas", key=f"like_{idx}"
                        ):
                            item.curtir()

                            # SALVA NO BANCO DE DADOS (JSON)
                            salvar_sistema_json(sistema)

                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    if not is_evento and hasattr(item, "comentarios"):
                        st.markdown(
                            '<div style="padding: 0px 14px;">',
                            unsafe_allow_html=True,
                        )

                        if item.comentarios:
                            for c in item.comentarios:
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

                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.form(
                            key=f"form_coment_{idx}", clear_on_submit=True
                        ):
                            c_input, c_btn = st.columns([0.8, 0.2])

                            with c_input:
                                txt_coment = st.text_input(
                                    "Adicionar comentário...",
                                    placeholder="Adicionar comentário como " + (aluno_logado.nome if aluno_logado else "visitante") + "...",
                                    label_visibility="collapsed",
                                    key=f"in_{idx}",
                                )

                            with c_btn:
                                if st.form_submit_button("Publicar"):
                                    if txt_coment.strip():
                                        if not aluno_logado:
                                            st.error("⚠️ Faça login para comentar.")
                                        else:
                                            autor_nome_c = aluno_logado.nome
                                            item.comentar(
                                                f"{autor_nome_c}::{txt_coment.strip()}"
                                            )

                                            # SALVA NO BANCO DE DADOS (JSON)
                                            salvar_sistema_json(sistema)

                                            st.rerun()

                    st.markdown("</div>", unsafe_allow_html=True)

    with tab_novo:
        st.subheader("O que você deseja compartilhar?")

        categoria = st.radio(
            "Tipo de Publicação",
            ["Post Geral", "Dúvida", "Material", "Evento"],
            horizontal=True,
        )

        if not aluno_logado and categoria != "Evento":
            st.warning(
                "⚠️ Faça login ou selecione o seu perfil de aluno na aba 'Alunos' antes de criar uma postagem."
            )
        else:
            with st.form("form_nova_pub", clear_on_submit=True):
                if categoria != "Evento":
                    st.info(f"👤 Publicando como: **{aluno_logado.nome}** (`{aluno_logado.matricula}`)")

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
                                foto_b64 = (
                                    uploaded_file_to_base64(foto_post_upload)
                                    if foto_post_upload
                                    else None
                                )

                                if categoria == "Post Geral":
                                    post = Postagem(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_logado,
                                    )
                                elif categoria == "Dúvida":
                                    post = PostagemDuvida(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_logado,
                                        disciplina=disciplina_nome.strip()
                                        or "Geral",
                                    )
                                else:
                                    post = PostagemMaterial(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_logado,
                                        link_download=link_download.strip()
                                        or "#",
                                    )

                                if foto_b64:
                                    setattr(post, "foto_post_b64", foto_b64)

                                sistema.adicionar_postagem(post)

                                # SALVA NO BANCO DE DADOS (JSON)
                                salvar_sistema_json(sistema)

                                st.success("✅ Publicado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao publicar: {str(e)}")

                else:
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

                                # SALVA NO BANCO DE DADOS (JSON)
                                salvar_sistema_json(sistema)

                                st.success("✅ Evento criado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao criar evento: {str(e)}")
# ==========================================================
# 6. TELA DE ESTATÍSTICAS E DASHBOARD
# ==========================================================
def tela_estatisticas(sistema):
    st.markdown(
        "<h1>📊 Dashboard de Estatísticas</h1>", unsafe_allow_html=True
    )
    st.write(
        "Acompanhe o engajamento da comunidade e as métricas do FocusU em tempo real."
    )

    alunos = list(sistema.alunos_por_matricula.values())
    postagens = sistema.postagens
    eventos = sistema.eventos

    total_alunos = len(alunos)
    total_posts = len(postagens)
    total_eventos = len(eventos)

    total_curtidas = sum(getattr(p, "curtidas", 0) for p in postagens)
    total_comentarios = sum(
        len(getattr(p, "comentarios", [])) for p in postagens
    )

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

    col_left, col_right = st.columns(2)

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

    if "pagina" not in st.session_state:
        st.session_state.pagina = "Home"

    with st.sidebar:
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

        botoes = [
            ("Home", "home"),
            ("Alunos", "user"),
            ("Disciplinas", "livro"),
            ("Agenda", "rotina"),
            ("Feed", "chat"),
            ("Estatísticas", "dashboard"),
        ]

        for nome, chave_icone in botoes:
            eh_ativa = st.session_state.pagina == nome
            tipo_botao = "primary" if eh_ativa else "secondary"

            img_icon = ICONS.get(chave_icone, "")

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

    opcao = st.session_state.pagina

    if opcao == "Home":
        tela_home(sistema)
    elif opcao == "Alunos":
        tela_alunos(sistema)
    elif opcao == "Disciplinas":
        tela_disciplinas(sistema)
    elif opcao == "Agenda":
        tela_agenda(sistema)
    elif opcao == "Feed":
        tela_feed(sistema)
    elif opcao == "Estatísticas":
        tela_estatisticas(sistema)
