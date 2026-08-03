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
            nome_aluno = getattr(aluno_logado, "nome", "Aluno")
            email_aluno = getattr(aluno_logado, "email", "Sem e-mail")
            matricula_aluno = getattr(aluno_logado, "matricula", "N/A")

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
                    inicial_p = nome_aluno[0].upper() if nome_aluno else "👤"
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
                st.markdown(f"<h3 style='margin:0; color:white;'>{nome_aluno}</h3>", unsafe_allow_html=True)
                st.caption(f"📧 {email_aluno}  |  🆔 Matrícula: **{matricula_aluno}**")

                minutos_estudo = 0
                try:
                    if hasattr(aluno_logado, "calcular_tempo_estudo_recursivo"):
                        minutos_estudo = aluno_logado.calcular_tempo_estudo_recursivo()
                except Exception:
                    minutos_estudo = 0

                horas = minutos_estudo // 60
                mins = minutos_estudo % 60
                st.markdown(f"⏱️ **Tempo Total Dedicado:** `{horas}h {mins}min`")

        # Progresso + Tarefas Pendentes + Tarefas Atrasadas
        col_prog, col_pend, col_atrasadas = st.columns(3)

        with col_prog:
            st.markdown("##### 📊 Progresso Acadêmico")
            progresso = 0.0
            try:
                if hasattr(aluno_logado, "calcular_progresso_estudos"):
                    progresso = aluno_logado.calcular_progresso_estudos(sistema)
            except Exception:
                progresso = 0.0

            try:
                val_progresso = float(progresso)
            except (ValueError, TypeError):
                val_progresso = 0.0

            st.progress(min(max(val_progresso / 100.0, 0.0), 1.0))
            st.caption(f"**{val_progresso}%** das atividades do sistema foram concluídas!")

        with col_pend:
            st.markdown("##### 📌 Tarefas Pendentes")
            tarefas_pendentes = []
            try:
                if hasattr(aluno_logado, "obter_tarefas_pendentes"):
                    tarefas_pendentes = aluno_logado.obter_tarefas_pendentes(sistema)
            except Exception:
                tarefas_pendentes = []

            if tarefas_pendentes and isinstance(tarefas_pendentes, list):
                for t in tarefas_pendentes[:2]:
                    if isinstance(t, dict):
                        titulo = t.get('titulo', 'Sem título')
                        disciplina = t.get('disciplina', 'Geral')
                        data = t.get('data_entrega', 'Sem data')
                        st.warning(f"**{titulo}** ({disciplina}) — Entrega: `{data}`")
            else:
                st.success("Nenhuma tarefa pendente no momento! 🎉")

        with col_atrasadas:
            st.markdown("##### ⚠️ Tarefas Atrasadas")
            tarefas_atrasadas = []
            try:
                if hasattr(aluno_logado, "obter_tarefas_atrasadas"):
                    tarefas_atrasadas = aluno_logado.obter_tarefas_atrasadas(sistema)
            except Exception:
                tarefas_atrasadas = []

            if tarefas_atrasadas and isinstance(tarefas_atrasadas, list):
                for t in tarefas_atrasadas[:2]:
                    if isinstance(t, dict):
                        titulo = t.get('titulo', 'Sem título')
                        disciplina = t.get('disciplina', 'Geral')
                        data = t.get('data_entrega', 'Sem data')
                        st.error(f"🚨 **{titulo}** ({disciplina}) — Venceu em: `{data}`")
            else:
                st.success("Tudo em dia! Nenhuma tarefa atrasada. 👏")

        st.divider()

        # Editar Perfil
        with st.expander("✏️ Editar Meu Perfil"):
            with st.form("form_editar_perfil"):
                novo_nome = st.text_input("Novo Nome", value=nome_aluno)
                novo_email = st.text_input("Novo E-mail", value=email_aluno)
                nova_foto = st.file_uploader("Trocar Foto", type=["png", "jpg", "jpeg"])

                if st.form_submit_button("Salvar Alterações", type="primary"):
                    try:
                        b64_foto = None
                        if nova_foto:
                            b64_foto = uploaded_file_to_base64(nova_foto)

                        if hasattr(aluno_logado, "atualizar_perfil"):
                            aluno_logado.atualizar_perfil(novo_nome, novo_email, b64_foto)
                        else:
                            aluno_logado.nome = novo_nome
                            aluno_logado.email = novo_email
                            if b64_foto:
                                aluno_logado.foto_b64 = b64_foto

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
                mat_limpa = str(matricula_login).strip()
                senha_limpa = str(senha_login).strip()

                if not mat_limpa or not senha_limpa:
                    st.warning("⚠️ Preencha a matrícula e a senha.")
                else:
                    aluno_encontrado = sistema.alunos_por_matricula.get(mat_limpa)
                    senha_salva = str(getattr(aluno_encontrado, "senha", "")).strip() if aluno_encontrado else ""

                    if aluno_encontrado and senha_salva == senha_limpa and senha_salva != "":
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
                mat_cad = str(matricula).strip()
                senha_cad = str(senha).strip()
                nome_cad = str(nome).strip()
                email_cad = str(email).strip()

                if not nome_cad or not email_cad or not mat_cad or not senha_cad:
                    st.warning("⚠️ Preencha todos os campos obrigatórios (incluindo a senha).")
                elif mat_cad in sistema.alunos_por_matricula:
                    st.error("❌ Esta matrícula já está cadastrada no sistema.")
                else:
                    try:
                        foto_b64 = uploaded_file_to_base64(foto_upload) if foto_upload else None

                        aluno = Aluno(nome=nome_cad, email=email_cad, matricula=mat_cad)

                        # Guarda a senha limpa no objeto
                        setattr(aluno, "senha", senha_cad)
                        if foto_b64:
                            setattr(aluno, "foto_b64", foto_b64)

                        sistema.adicionar_aluno(aluno)
                        salvar_sistema_json(sistema)

                        st.session_state["aluno_logado"] = aluno

                        st.success(f"✅ Conta criada com sucesso! Bem-vindo(a), {nome_cad}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar: {str(e)}")


# ==========================================================
# 3. TELA DISCIPLINAS
# ==========================================================
def tela_disciplinas(sistema):
    st.markdown("<h1>Gerenciamento de Disciplinas</h1>", unsafe_allow_html=True)
    st.write("Cadastre novas disciplinas no sistema e matricule-se para criar sua grade.")

    aluno_logado = st.session_state.get("aluno_logado", None)
    lista_disc_global = list(sistema.disciplinas_por_nome.values())

    tab_matricular, tab_criar, tab_listar = st.tabs(["📌 Me Matricular", "➕ Cadastrar Nova", "📖 Ver Todas"])

    # --- ABA MATRICULAR ---
    with tab_matricular:
        if not aluno_logado:
            st.warning("⚠️ Você precisa fazer login na aba 'Alunos' para se matricular em uma disciplina.")
        else:
            st.subheader("Vincular disciplina ao meu perfil")
            if not lista_disc_global:
                st.info("Não há disciplinas no sistema. Cadastre uma na aba ao lado.")
            else:
                nomes_disciplinas = [d.nome for d in lista_disc_global]
                disc_escolhida = st.selectbox("Escolha uma disciplina disponível:", nomes_disciplinas)
                
                if st.button("Confirmar Matrícula", type="primary"):
                    # Busca a disciplina diretamente na lista
                    disciplina_obj = next(d for d in lista_disc_global if d.nome == disc_escolhida)
                    
                    # Verifica se o aluno já tem essa disciplina para evitar duplicatas
                    já_matriculado = any(d.nome == disc_escolhida for d in aluno_logado.disciplinas)
                    
                    if já_matriculado:
                        st.warning("Você já está matriculado nesta disciplina!")
                    else:
                        # 1. Adiciona a disciplina no perfil do aluno
                        aluno_logado.adicionar_disciplina(disciplina_obj)
                        
                        # 2. Salva a matrícula do aluno dentro da disciplina (cadeira)
                        if not hasattr(disciplina_obj, "alunos_matriculados"):
                            disciplina_obj.alunos_matriculados = []
                            
                        if aluno_logado.matricula not in disciplina_obj.alunos_matriculados:
                            disciplina_obj.alunos_matriculados.append(aluno_logado.matricula)
                            
                        salvar_sistema_json(sistema)
                        st.success(f"✅ Matrícula em **{disc_escolhida}** realizada com sucesso!")
                        st.rerun()

            st.divider()
            
            # --- NOVA SEÇÃO: GERENCIAR MATRÍCULAS ATIVAS ---
            st.subheader("Minhas Matrículas Ativas")
            
            if not getattr(aluno_logado, "disciplinas", []):
                st.info("Você ainda não está matriculado em nenhuma disciplina.")
            else:
                for disc in aluno_logado.disciplinas:
                    col_nome, col_btn = st.columns([0.75, 0.25])
                    with col_nome:
                        st.markdown(f"📖 **{disc.nome}**")
                    with col_btn:
                        # O botão precisa de uma chave única (key) baseada no nome da disciplina
                        if st.button("Encerrar Matrícula", key=f"desmatricular_{disc.nome}"):
                            
                            # 1. Remove a disciplina da lista do aluno
                            aluno_logado.disciplinas = [d for d in aluno_logado.disciplinas if d.nome != disc.nome]
                            
                            # 2. Remove a matrícula do aluno da cadeira global
                            disc_global = next((d for d in lista_disc_global if d.nome == disc.nome), None)
                            if disc_global and hasattr(disc_global, "alunos_matriculados"):
                                if aluno_logado.matricula in disc_global.alunos_matriculados:
                                    disc_global.alunos_matriculados.remove(aluno_logado.matricula)
                            
                            # 3. Salva as alterações no JSON e recarrega a página
                            salvar_sistema_json(sistema)
                            st.rerun()
                    
                    st.markdown("<hr style='margin: 0.5em 0px; border-color: #333;'>", unsafe_allow_html=True)

    # --- ABA CRIAR ---
    with tab_criar:
        st.subheader("Cadastrar Disciplina no Sistema")
        with st.form("cadastro_disciplina", clear_on_submit=True):
            nome = st.text_input("Nome da Disciplina", placeholder="Ex: Programação Orientada a Objetos")
            professor = st.text_input("Professor Responsável", placeholder="Ex: Dr. Alan Turing")
            cadastrar = st.form_submit_button("Cadastrar Disciplina", use_container_width=True, type="primary")

        if cadastrar:
            if not nome.strip() or not professor.strip():
                st.warning("⚠️ Preencha o nome da disciplina e o professor.")
            else:
                try:
                    disciplina = Disciplina(nome=nome.strip(), professor=professor.strip())
                    sistema.adicionar_disciplina_global(disciplina)
                    salvar_sistema_json(sistema)
                    st.success(f"✅ Disciplina **{nome}** cadastrada no sistema!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")

    # --- ABA LISTAR ---
    with tab_listar:
        st.subheader(f"Disciplinas Cadastradas ({len(lista_disc_global)})")
        if lista_disc_global:
            for disc in lista_disc_global:
                with st.container(border=True):
                    st.markdown(f"<h4 style='margin:0; color:white;'>{disc.nome}</h4>", unsafe_allow_html=True)
                    
                    # Conta quantos alunos estão matriculados nesta cadeira
                    qtd_alunos = len(getattr(disc, "alunos_matriculados", []))
                    
                    st.caption(f"👨‍🏫 **Professor Responsável:** {disc.professor}  |  👥 **Alunos Matriculados:** {qtd_alunos}")
        else:
            st.info("Nenhuma disciplina cadastrada no momento.")


# ==========================================================
# 4. TELA AGENDA (Isolada por aluno)
# ==========================================================
def tela_agenda(sistema):
    st.markdown("<h1>📅 Minha Agenda Privada</h1>", unsafe_allow_html=True)
    
    aluno_logado = st.session_state.get("aluno_logado", None)
    if not aluno_logado:
        st.warning("⚠️ Você precisa fazer login na aba 'Alunos' para acessar suas tarefas.")
        return

    st.write("Acompanhe suas provas, entregas e trabalhos organizados por disciplina.")

    # SEGURANÇA: Carrega APENAS as disciplinas do aluno logado
    dict_disciplinas = {d.nome: d for d in getattr(aluno_logado, "disciplinas", [])}

    if not dict_disciplinas:
        st.warning("⚠️ Você ainda não está matriculado em nenhuma disciplina. Vá na aba 'Disciplinas' para se matricular.")
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
                    
                    if hasattr(disciplina_obj, "adicionar_tarefa"):
                        tarefa_criada = disciplina_obj.adicionar_tarefa(
                            titulo=titulo.strip(),
                            data_entrega=data_entrega,
                            tipo=tipo,
                            descricao=descricao.strip()
                        )
                        
                        # --- INÍCIO DA CORREÇÃO: Vincula a tarefa ao aluno logado ---
                        if tarefa_criada:
                            if isinstance(tarefa_criada, dict):
                                tarefa_criada["dono"] = aluno_logado.matricula
                            else:
                                tarefa_criada.dono = aluno_logado.matricula
                        else:
                            # Fallback caso a função não retorne o objeto diretamente
                            try:
                                if hasattr(disciplina_obj, "listar_tarefas"):
                                    todas_t = disciplina_obj.listar_tarefas()
                                    if todas_t:
                                        if isinstance(todas_t[-1], dict):
                                            todas_t[-1]["dono"] = aluno_logado.matricula
                                        else:
                                            todas_t[-1].dono = aluno_logado.matricula
                            except Exception:
                                pass
                        # --- FIM DA CORREÇÃO ---
                        
                        salvar_sistema_json(sistema)
                        st.success(f"✅ Tarefa adicionada à disciplina **{nome_disc_selecionada}**!")
                        st.rerun()
                    else:
                        st.error("Erro no objeto da disciplina. Recarregue a página ou cadastre novamente.")

    st.markdown("### 📚 Minhas Tarefas por Disciplina")

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
        if hasattr(disciplina_obj, "listar_tarefas") and callable(getattr(disciplina_obj, "listar_tarefas")):
            tarefas_brutas = disciplina_obj.listar_tarefas(status=status_param)
        elif isinstance(disciplina_obj, dict):
            dict_t = disciplina_obj.get("_tarefas", {})
            tarefas_brutas = list(dict_t.values()) if isinstance(dict_t, dict) else dict_t
        else:
            tarefas_brutas = []

        # --- INÍCIO DA CORREÇÃO: Filtra apenas as tarefas deste usuário ---
        tarefas_do_aluno = []
        for t in tarefas_brutas:
            dono = getattr(t, "dono", t.get("dono") if isinstance(t, dict) else None)
            
            # Mostra se for do aluno logado OU se não tiver dono (tarefas criadas antes desta correção)
            if dono == aluno_logado.matricula or dono is None:
                tarefas_do_aluno.append(t)
        # --- FIM DA CORREÇÃO ---

        if filtro_status == "Pendentes":
            tarefas = [t for t in tarefas_do_aluno if not getattr(t, "concluida", False)]
        elif filtro_status == "Concluídas":
            tarefas = [t for t in tarefas_do_aluno if getattr(t, "concluida", False)]
        else:
            tarefas = tarefas_do_aluno

        with st.expander(f"📖 **{nome_disc}** ({len(tarefas)} tarefas)", expanded=True):
            if not tarefas:
                st.caption("Nenhuma tarefa encontrada para os filtros selecionados.")
                continue

            for tarefa in tarefas:
                col_check, col_info = st.columns([0.08, 0.92])

                t_id = getattr(tarefa, "id", tarefa.get("id") if isinstance(tarefa, dict) else None)
                t_tipo = getattr(tarefa, "tipo", tarefa.get("tipo", "Geral") if isinstance(tarefa, dict) else "Geral")
                t_titulo = getattr(tarefa, "titulo", tarefa.get("titulo", "") if isinstance(tarefa, dict) else "")
                t_data = getattr(tarefa, "data_entrega", tarefa.get("data_entrega") if isinstance(tarefa, dict) else None)
                t_desc = getattr(tarefa, "descricao", tarefa.get("descricao", "") if isinstance(tarefa, dict) else "")
                ja_concluida = getattr(tarefa, "concluida", tarefa.get("concluida", False) if isinstance(tarefa, dict) else False)

                with col_check:
                    marcado = st.checkbox(
                        label="Concluir",
                        value=ja_concluida,
                        key=f"chk_{t_id}",
                        label_visibility="collapsed"
                    )

                    if marcado != ja_concluida:
                        if marcado:
                            if hasattr(disciplina_obj, "concluir_tarefa"):
                                disciplina_obj.concluir_tarefa(t_id)
                            elif isinstance(tarefa, dict):
                                tarefa["concluida"] = True
                            else:
                                tarefa.concluida = True
                        else:
                            if isinstance(tarefa, dict):
                                tarefa["concluida"] = False
                            else:
                                tarefa.concluida = False

                        salvar_sistema_json(sistema)
                        st.rerun()

                with col_info:
                    icone = icones_tipo.get(t_tipo, "📌")
                    data_str = t_data.strftime("%d/%m/%Y") if hasattr(t_data, "strftime") else str(t_data)

                    if ja_concluida:
                        st.markdown(f"~~{icone} **[{t_tipo}]** {t_titulo} — *Vencimento: {data_str}*~~")
                    else:
                        st.markdown(f"{icone} **[{t_tipo}]** **{t_titulo}** — 🗓️ *Vencimento: {data_str}*")

                    if t_desc:
                        st.caption(f"💬 {t_desc}")

                    if not ja_concluida and isinstance(t_data, date) and t_data < date.today():
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
                        "Institucional" if is_evento else "clara",
                    )
                    foto_autor = getattr(autor_obj, "foto_b64", None)
                    foto_post = getattr(item, "foto_post_b64", None)

                    # Construção do Avatar
                    if foto_autor:
                        avatar_html = f'<img src="{foto_autor}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">'
                    else:
                        letra = nome_autor[0].upper() if nome_autor else "I"
                        avatar_html = f"""
                        <div style="
                            background: linear-gradient(135deg, #C13584, #E1306C, #FD1D1D);
                            width: 32px; height: 32px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: bold; font-size: 14px;
                        ">{letra}</div>
                        """

                    # Renderiza o Cabeçalho do Card
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #121214;
                            border: 1px solid #27272A;
                            border-radius: 10px;
                            margin-bottom: 28px;
                            padding-bottom: 12px;
                            overflow: hidden;
                        ">
                            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 14px;">
                                {avatar_html}
                                <span style="color: white; font-weight: 600; font-size: 14px;">{nome_autor.lower()}</span>
                            </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Se for foto do post
                    if foto_post:
                        st.markdown(
                            f"""
                            <div style="width: 100%; background: #000; text-align: center;">
                                <img src="{foto_post}" style="width: 100%; max-height: 600px; object-fit: contain;">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    # Título e Conteúdo do Card
                    st.markdown('<div style="padding: 10px 14px 0px 14px;">', unsafe_allow_html=True)

                    if hasattr(item, "titulo") and item.titulo:
                        st.markdown(
                            f"<h4 style='color: white; margin: 0 0 4px 0;'>{item.titulo}</h4>",
                            unsafe_allow_html=True,
                        )

                    # Se for EVENTO, exibe data e hora
                    if is_evento:
                        data_ev = getattr(item, "data", "A definir")
                        hora_ev = getattr(item, "horario", "A definir")
                        st.markdown(
                            f"""
                            <p style='color: #A1A1AA; font-size: 14px; margin: 4px 0;'>
                                📅 <strong>Data:</strong> {data_ev} &nbsp;|&nbsp; ⏰ <strong>Horário:</strong> {hora_ev}
                            </p>
                            """,
                            unsafe_allow_html=True,
                        )

                    conteudo_texto = getattr(item, "conteudo", "")
                    if conteudo_texto:
                        st.markdown(
                            f"<p style='color: #E4E4E7; font-size: 14px; margin: 0;'><strong style='color:white;'>{nome_autor.lower()}</strong> {conteudo_texto}</p>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

                    # ==========================================================
                    # LÓGICA DE CURTIDA ÚNICA COM TOGGLE (APENAS PARA POSTS)
                    # ==========================================================
                    if not is_evento:
                        st.markdown('<div style="padding: 6px 14px;">', unsafe_allow_html=True)

                        if not hasattr(item, "curtidores") or not isinstance(item.curtidores, set):
                            if hasattr(item, "curtidores") and isinstance(item.curtidores, list):
                                item.curtidores = set(item.curtidores)
                            else:
                                item.curtidores = set()

                        user_id = getattr(aluno_logado, "matricula", None) if aluno_logado else "anonimo"
                        ja_curtiu = user_id in item.curtidores
                        icone_like = "❤️" if ja_curtiu else "🤍"
                        total_likes = len(item.curtidores) if item.curtidores else getattr(item, "curtidas", 0)

                        if st.button(f"{icone_like} {total_likes} curtidas", key=f"like_{idx}"):
                            if not aluno_logado:
                                st.warning("⚠️ Faça login para curtir esta publicação.")
                            else:
                                if ja_curtiu:
                                    item.curtidores.remove(user_id)
                                else:
                                    item.curtidores.add(user_id)

                                item.curtidas = len(item.curtidores)
                                item.curtidores_list = list(item.curtidores)
                                salvar_sistema_json(sistema)
                                st.rerun()

                        st.markdown("</div>", unsafe_allow_html=True)

                    # Comentários (Apenas Posts)
                    if not is_evento and hasattr(item, "comentarios"):
                        st.markdown('<div style="padding: 0px 14px;">', unsafe_allow_html=True)

                        if item.comentarios:
                            for c in item.comentarios:
                                if "::" in str(c):
                                    c_autor, c_texto = str(c).split("::", 1)
                                else:
                                    c_autor, c_texto = (nome_autor.lower(), str(c))

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
                        with st.form(key=f"form_coment_{idx}", clear_on_submit=True):
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
                                            item.comentar(f"{autor_nome_c}::{txt_coment.strip()}")
                                            salvar_sistema_json(sistema)
                                            st.rerun()

                    # Fecha o Container principal do Card (Post ou Evento)
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

                    titulo = st.text_input("Título", placeholder="Ex: Foto no campus")
                    conteudo = st.text_area("Legenda", placeholder="Escreva a legenda...")
                    foto_post_upload = st.file_uploader("Anexar Foto", type=["png", "jpg", "jpeg"])

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
                                        disciplina=disciplina_nome.strip() or "Geral",
                                    )
                                else:
                                    post = PostagemMaterial(
                                        titulo=titulo.strip(),
                                        conteudo=conteudo.strip(),
                                        autor=aluno_logado,
                                        link_download=link_download.strip() or "#",
                                    )

                                if foto_b64:
                                    setattr(post, "foto_post_b64", foto_b64)

                                sistema.adicionar_postagem(post)
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