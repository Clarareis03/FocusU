import json
import os
from datetime import datetime, date

# Import das classes para recriar os objetos reais
from models.usuario import Aluno
from models.disciplina import Disciplina
from models.rotina import Rotina
from models.postagem import Postagem, PostagemDuvida, PostagemMaterial
from models.evento import Evento

ARQUIVO_BANCO = "dados_focusu.json"

# ==========================================================
# 1. SERIALIZAÇÃO (OBJETOS -> DICIONÁRIO)
# ==========================================================

def sistema_para_dict(sistema):
    """
    Converte o objeto SistemaFocusU e seus componentes em um dicionário puro.
    """
    dados = {
        "alunos": [],
        "disciplinas": [],
        "postagens": [],
        "eventos": []
    }

    # A) Converte Alunos (com Senha, Disciplinas, Rotinas e Foto)
    for aluno in sistema.alunos_por_matricula.values():
        aluno_data = {
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": str(aluno.matricula).strip(),
            "senha": getattr(aluno, "senha", ""),
            "foto_b64": getattr(aluno, "foto_b64", ""),
            "disciplinas": [d.nome for d in getattr(aluno, "disciplinas", [])],
            "rotinas": [
                {"atividade": r.atividade, "tempo": r.tempo}
                for r in getattr(aluno, 'rotinas', [])
            ]
        }
        dados["alunos"].append(aluno_data)

    # B) Converte Disciplinas (com Tarefas e Alunos Matriculados)
    for disc in sistema.disciplinas_por_nome.values():
        disc_data = {
            "nome": disc.nome,
            "professor": disc.professor,
            "alunos_matriculados": getattr(disc, "alunos_matriculados", []),
            "tarefas": [
                {
                    "titulo": t.titulo,
                    "data_entrega": t.data_entrega.strftime("%Y-%m-%d") if isinstance(t.data_entrega, (datetime, date)) else str(t.data_entrega),
                    "tipo": t.tipo,
                    "descricao": getattr(t, 'descricao', ''),
                    "concluida": getattr(t, 'concluida', False),
                    "dono": getattr(t, 'dono', None)
                }
                for t in disc.listar_tarefas()
            ]
        }
        dados["disciplinas"].append(disc_data)

    # C) Converte Postagens (Geral, Dúvida, Material + Foto + Curtidores)
    for post in sistema.postagens:
        curtidores_list = getattr(post, "curtidores", [])
        if isinstance(curtidores_list, set):
            curtidores_list = list(curtidores_list)

        autor_mat = None
        if getattr(post, "autor", None):
            autor_mat = str(post.autor.matricula).strip()

        post_data = {
            "tipo": post.__class__.__name__,
            "titulo": post.titulo,
            "conteudo": post.conteudo,
            "autor_matricula": autor_mat,
            "curtidas": getattr(post, "curtidas", len(curtidores_list)),
            "curtidores": curtidores_list,
            "comentarios": getattr(post, "comentarios", []),
            "foto_post_b64": getattr(post, "foto_post_b64", "")
        }
        if isinstance(post, PostagemDuvida):
            post_data["disciplina"] = post.disciplina
            post_data["resolvida"] = getattr(post, "resolvida", False)
        elif isinstance(post, PostagemMaterial):
            post_data["link_download"] = post.link_download

        dados["postagens"].append(post_data)

    # D) Converte Eventos
    for ev in sistema.eventos:
        dados["eventos"].append({
            "titulo": ev.titulo,
            "data": str(ev.data),
            "horario": str(ev.horario)
        })

    return dados


# ==========================================================
# 2. DESSERIALIZAÇÃO (DICIONÁRIO -> OBJETOS)
# ==========================================================

def dict_para_sistema(dados_dict, sistema):
    """
    Lê o dicionário salvo no JSON e recria as instâncias das classes no Sistema.
    """
    if not dados_dict:
        return sistema

    # Limpa dados anteriores na memória
    sistema.alunos_por_matricula = {}
    sistema.disciplinas_por_nome = {}
    sistema.postagens = []
    sistema.eventos = []

    # A) Recria Disciplinas
    for d in dados_dict.get("disciplinas", []):
        try:
            nova_disc = Disciplina(d["nome"], d["professor"])
            nova_disc.alunos_matriculados = d.get("alunos_matriculados", [])

            for t in d.get("tarefas", []):
                dt = t["data_entrega"]
                try:
                    dt = datetime.strptime(dt, "%Y-%m-%d").date()
                except Exception:
                    pass

                tarefa_criada = nova_disc.adicionar_tarefa(
                    titulo=t["titulo"],
                    data_entrega=dt,
                    tipo=t["tipo"],
                    descricao=t.get("descricao", "")
                )
                if t.get("dono"):
                    tarefa_criada.dono = t.get("dono")

                if t.get("concluida"):
                    nova_disc.concluir_tarefa(tarefa_criada.id)

            sistema.adicionar_disciplina_global(nova_disc)
        except Exception as e:
            print(f"Erro ao carregar disciplina '{d.get('nome')}': {e}")

    # B) Recria Alunos e vincula Disciplinas
    for a in dados_dict.get("alunos", []):
        try:
            mat_str = str(a["matricula"]).strip()
            novo_aluno = Aluno(a["nome"], a["email"], mat_str)
            
            if "senha" in a:
                setattr(novo_aluno, "senha", a["senha"])

            if a.get("foto_b64"):
                setattr(novo_aluno, "foto_b64", a["foto_b64"])

            for r in a.get("rotinas", []):
                novo_aluno.adicionar_rotina(Rotina(r["atividade"], r["tempo"]))

            # Restaura disciplinas vinculadas ao aluno
            for disc_nome in a.get("disciplinas", []):
                disc_obj = sistema.disciplinas_por_nome.get(disc_nome)
                if disc_obj:
                    novo_aluno.adicionar_disciplina(disc_obj)

            sistema.adicionar_aluno(novo_aluno)
        except Exception as e:
            print(f"Erro ao carregar aluno '{a.get('nome')}': {e}")

    # C) Recria Postagens
    for p in dados_dict.get("postagens", []):
        try:
            autor_mat = str(p.get("autor_matricula", "")).strip()
            autor_obj = sistema.alunos_por_matricula.get(autor_mat)
            tipo_post = p.get("tipo")

            if tipo_post == "PostagemDuvida":
                nova_post = PostagemDuvida(p["titulo"], p["conteudo"], autor_obj, p.get("disciplina", "Geral"))
                nova_post.resolvida = p.get("resolvida", False)
            elif tipo_post == "PostagemMaterial":
                nova_post = PostagemMaterial(p["titulo"], p["conteudo"], autor_obj, p.get("link_download", ""))
            else:
                nova_post = Postagem(p["titulo"], p["conteudo"], autor_obj)

            nova_post.curtidores = p.get("curtidores", [])
            nova_post.curtidas = len(nova_post.curtidores) if nova_post.curtidores else p.get("curtidas", 0)
            nova_post.comentarios = p.get("comentarios", [])

            if p.get("foto_post_b64"):
                setattr(nova_post, "foto_post_b64", p["foto_post_b64"])

            sistema.adicionar_postagem(nova_post)
        except Exception as e:
            print(f"Erro ao carregar postagem '{p.get('titulo')}': {e}")

    # D) Recria Eventos
    for ev in dados_dict.get("eventos", []):
        try:
            novo_ev = Evento(ev["titulo"], ev["data"], ev["horario"])
            sistema.adicionar_evento(novo_ev)
        except Exception as e:
            print(f"Erro ao carregar evento '{ev.get('titulo')}': {e}")

    return sistema


# ==========================================================
# 3. SALVAR E CARREGAR NO DISCO (JSON)
# ==========================================================

def salvar_sistema_json(sistema):
    """Salva o estado atual do sistema no arquivo JSON."""
    try:
        dados_dict = sistema_para_dict(sistema)
        with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
            json.dump(dados_dict, f, ensure_ascii=False, indent=4)
        print("💾 Sistema salvo com sucesso no banco JSON!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar sistema: {e}")
        return False

def carregar_sistema_json(sistema):
    """Carrega os dados salvos do JSON para o sistema."""
    if not os.path.exists(ARQUIVO_BANCO):
        print("⚠️ Nenhum banco JSON existente encontrado. Iniciando zerado.")
        return sistema

    try:
        with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
            dados_dict = json.load(f)
            dict_para_sistema(dados_dict, sistema)
            print("📂 Dados do JSON carregados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo de dados: {e}")

    return sistema