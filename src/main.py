# -*- coding: utf-8 -*-

from models.usuario import Aluno
from models.disciplina import Disciplina
from models.rotina import Rotina
from models.postagem import (
    Postagem,
    PostagemDuvida,
    PostagemMaterial
)
from models.evento import Evento
from system.sistema import SistemaFocusU

# Importa as funções de persistência para manter o JSON atualizado
try:
    from src.utils.persistencia import carregar_sistema_json, salvar_sistema_json
except ModuleNotFoundError:
    try:
        from utils.persistencia import carregar_sistema_json, salvar_sistema_json
    except ModuleNotFoundError:
        from persistencia import carregar_sistema_json, salvar_sistema_json

# Inicializa o sistema carregando os dados do JSON (se houver)
instancia_sistema = SistemaFocusU()
sistema = carregar_sistema_json(instancia_sistema)

# Variável de Sessão (Controla quem está logado no terminal)
aluno_logado = None

while True:
    print("\n════════════════════════════")
    print("        FOCUS U 2.0")
    print("════════════════════════════")

    # ==============================================================
    # TELA DE ACESSO (USUÁRIO DESLOGADO)
    # ==============================================================
    if aluno_logado is None:
        print("1 - Login")
        print("2 - Cadastro de Nova Conta")
        print("3 - Esqueci Minha Senha")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("\nSaindo do Focus U... Até logo!")
            break

        elif opcao == "1":
            print("\n--- LOGIN ---")
            mat = input("Matrícula: ").strip()
            senha = input("Senha: ").strip()

            # Busca o aluno no sistema pela matrícula
            aluno_encontrado = sistema.alunos_por_matricula.get(mat)

            if aluno_encontrado and aluno_encontrado.verificar_senha(senha):
                aluno_logado = aluno_encontrado
                print(f"\nLogin efetuado com sucesso! Bem-vindo(a), {aluno_logado.nome}.")
            else:
                print("\n[ERRO]: Matrícula ou senha incorretos.")

        elif opcao == "2":
            print("\n--- CADASTRO ---")
            mat = input("Matrícula: ").strip()
            nome = input("Nome de Usuário: ").strip()
            email = input("Email: ").strip()
            senha = input("Senha (min. 3 caracteres): ").strip()

            if not mat or not nome or not email or not senha:
                print("\n[AÇÃO CANCELADA]: Todos os campos devem ser preenchidos.")
                continue

            if mat in sistema.alunos_por_matricula:
                print("\n[AÇÃO CANCELADA]: Esta matrícula já está cadastrada.")
                continue

            try:
                novo_aluno = Aluno(nome, email, mat, senha)
                sistema.adicionar_aluno(novo_aluno)
                salvar_sistema_json(sistema) # Persiste o novo cadastro
                print("\nAluno cadastrado com sucesso! Você já pode fazer login.")
            except ValueError as e:
                print(f"\n[ERRO NO CADASTRO]: {e}")
                
        elif opcao == "3":
            print("\n--- RECUPERAÇÃO DE SENHA ---")
            email_rec = input("Seu E-mail cadastrado: ").strip()
            mat_rec = input("Sua Matrícula: ").strip()
            nova_senha = input("Nova Senha (min. 3 caracteres): ").strip()
            
            if not email_rec or not mat_rec or not nova_senha:
                print("\n[AÇÃO CANCELADA]: Todos os campos devem ser preenchidos.")
                continue
                
            if sistema.redefinir_senha(email_rec, mat_rec, nova_senha):
                salvar_sistema_json(sistema) # Persiste a nova senha
                print("\nSenha alterada com sucesso! Você já pode fazer login.")
            else:
                print("\n[ERRO]: E-mail ou matrícula não encontrados/não coincidem.")
        
        else:
            print("\n[OPÇÃO INVÁLIDA]: Escolha uma das opções do menu.")

    # ==============================================================
    # ÁREA LOGADA (O USUÁRIO SÓ VÊ ISSO SE TIVER FEITO LOGIN)
    # ==============================================================
    else:
        print(f"\n--- Usuário: {aluno_logado.nome} | Matrícula: {aluno_logado.matricula} ---")
        print("1 - Criar Disciplina Geral (Sistema)")
        print("2 - Me Matricular em uma Disciplina")
        print("3 - Adicionar Rotina de Estudo")
        print("4 - Criar Postagem no Feed")
        print("5 - Criar Evento no Sistema")
        print("6 - Exibir Feed Geral")
        print("7 - Ver MINHAS Tarefas Pendentes")
        print("8 - Curtir Postagem")
        print("9 - Comentar Postagem")
        print("10 - Listar Todos os Alunos")
        print("11 - Estatísticas Gerais do Sistema")
        print("12 - [RECURSÃO] Meu Tempo de Estudo Total")
        print("13 - Apagar Minha Conta")
        print("14 - Apagar Minha Postagem")
        print("15 - Sair da Conta (Logout)")
        print("0 - Encerrar Programa")

        opcao = input("\nEscolha uma opção: ").strip()
        OPCOES_VALIDAS = {str(i) for i in range(16)}

        if opcao not in OPCOES_VALIDAS:
            print("\n[OPÇÃO INVÁLIDA]: Escolha um número válido do menu.")
            continue

        try:
            if opcao == "1":
                nome = input("Disciplina: ").strip()
                prof = input("Professor: ").strip()
                if not nome or not prof:
                    print("\n[AÇÃO CANCELADA]: Preencha tudo.")
                    continue
                sistema.adicionar_disciplina_global(Disciplina(nome, prof))
                salvar_sistema_json(sistema)
                print("\nDisciplina criada no sistema global!")

            elif opcao == "2":
                lista_disciplinas = list(sistema.disciplinas_por_nome.values())
                if not lista_disciplinas:
                    print("\nNão há disciplinas cadastradas no sistema ainda.")
                    continue

                print("\nDisciplinas disponíveis:")
                for i, d in enumerate(lista_disciplinas): 
                    print(f"{i} - {d.nome} (Prof. {d.professor if hasattr(d, 'professor') else 'Desconhecido'})")
                
                idx_d = int(input("Escolha a disciplina pelo número: "))
                if idx_d < 0 or idx_d >= len(lista_disciplinas):
                    print("\n[ERRO]: Número de disciplina inválido.")
                    continue

                # Associa a disciplina ao aluno logado
                disciplina_escolhida = lista_disciplinas[idx_d]
                aluno_logado.adicionar_disciplina(disciplina_escolhida)

                if not hasattr(disciplina_escolhida, "alunos_matriculados") or disciplina_escolhida.alunos_matriculados is None:
                    disciplina_escolhida.alunos_matriculados = []
                if str(aluno_logado.matricula) not in disciplina_escolhida.alunos_matriculados:
                    disciplina_escolhida.alunos_matriculados.append(str(aluno_logado.matricula))

                salvar_sistema_json(sistema)
                print("\nMatrícula na disciplina efetuada com sucesso!")

            elif opcao == "3":
                atv = input("Atividade: ").strip()
                temp_raw = input("Tempo em minutos (ex: 30): ").strip().lower()
                temp_raw = temp_raw.replace("minutos", "").replace("min", "").replace("m", "").strip()
                temp = int(temp_raw)

                if temp <= 0:
                    print("\n[AÇÃO CANCELADA]: O tempo deve ser maior que 0.")
                    continue

                aluno_logado.adicionar_rotina(Rotina(atv, temp))
                salvar_sistema_json(sistema)
                print("\nRotina salva no SEU perfil pessoal!")

            elif opcao == "4":
                print("\nTipo: 1-Geral | 2-Dúvida | 3-Material")
                tipo = input("Escolha: ").strip()
                t, c = input("Título: ").strip(), input("Conteúdo: ").strip()

                if tipo == "2":
                    disc = input("Disciplina da dúvida: ").strip()
                    p = PostagemDuvida(t, c, aluno_logado, disc)
                elif tipo == "3":
                    link = input("Link do material: ").strip()
                    p = PostagemMaterial(t, c, aluno_logado, link)
                else:
                    p = Postagem(t, c, aluno_logado)

                sistema.adicionar_postagem(p)
                salvar_sistema_json(sistema)
                print("\nPostagem enviada ao feed!")

            elif opcao == "5":
                t, d, h = input("Título: ").strip(), input("Data: ").strip(), input("Horário: ").strip()
                sistema.adicionar_evento(Evento(t, d, h))
                salvar_sistema_json(sistema)
                print("\nEvento publicado!")

            elif opcao == "6": 
                sistema.exibir_feed()

            elif opcao == "7":
                tarefas = aluno_logado.obter_tarefas_pendentes()
                print(f"\n--- TAREFAS DE {aluno_logado.nome.upper()} ---")
                if not tarefas:
                    print("Você não possui tarefas pendentes! Tudo em dia.")
                else:
                    for t in tarefas:
                        print(f"• [{t['disciplina']}] {t['titulo']} (Entrega: {t['data_entrega']})")

            elif opcao == "8":
                if not sistema.postagens: 
                    print("\nNenhum post disponível.")
                    continue
                for i, p in enumerate(sistema.postagens): 
                    print(f"{i} - {p.titulo}")
                
                idx = int(input("\nEscolha o post (número): "))
                if idx < 0 or idx >= len(sistema.postagens):
                    print("\n[ERRO]: Índice de post fora da lista.")
                    continue
                
                sistema.postagens[idx].curtir()
                salvar_sistema_json(sistema)
                print("\nVocê curtiu essa publicação!")

            elif opcao == "9":
                if not sistema.postagens: 
                    print("\nNenhum post disponível.")
                    continue
                for i, p in enumerate(sistema.postagens): 
                    print(f"{i} - {p.titulo}")
                
                idx = int(input("\nEscolha o post (número): "))
                if idx < 0 or idx >= len(sistema.postagens):
                    print("\n[ERRO]: Índice de post fora da lista.")
                    continue
                    
                coment = input("Seu Comentário: ").strip()
                sistema.postagens[idx].comentar(coment)
                salvar_sistema_json(sistema)
                print("\nComentário publicado!")

            elif opcao == "10": 
                sistema.listar_alunos()

            elif opcao == "11": 
                sistema.estatisticas()

            elif opcao == "12":
                total_minutos = aluno_logado.calcular_tempo_estudo_recursivo()
                horas = total_minutos // 60
                minutos = total_minutos % 60
                print(f"\n[CÁLCULO RECURSIVO]: Você acumula {total_minutos} min de estudos ({horas}h {minutos}min).")

            elif opcao == "13":
                confirmacao = input("Tem certeza que deseja apagar SUA conta? (s/n): ").strip().lower()
                if confirmacao == 's':
                    sistema.remover_aluno(aluno_logado)
                    salvar_sistema_json(sistema)
                    print(f"\nSua conta ({aluno_logado.nome}) foi apagada.")
                    aluno_logado = None 
                else:
                    print("\nAção cancelada.")

            elif opcao == "14":
                minhas_postagens = [p for p in sistema.postagens if getattr(p, 'autor', None) == aluno_logado]
                
                if not minhas_postagens:
                    print("\nVocê não tem nenhuma postagem publicada no momento.")
                    continue
                    
                print("\n--- SUAS POSTAGENS ---")
                for i, p in enumerate(minhas_postagens):
                    print(f"{i} - {p.titulo}")
                    
                idx_post = int(input("\nDigite o número da postagem que deseja apagar: "))
                
                if idx_post < 0 or idx_post >= len(minhas_postagens):
                    print("\n[ERRO]: Número de postagem inválido.")
                    continue
                    
                post_para_remover = minhas_postagens[idx_post]
                
                if sistema.remover_postagem(post_para_remover):
                    salvar_sistema_json(sistema)
                    print("\nPostagem removida com sucesso!")
                else:
                    print("\n[ERRO]: Não foi possível remover a postagem.")

            elif opcao == "15":
                print(f"\nAté logo, {aluno_logado.nome}! Deslogando...")
                aluno_logado = None 

            elif opcao == "0":
                print("\nSaindo do Focus U... Até logo!")
                break

        except ValueError as erro_val:
            texto_erro = str(erro_val)
            if "invalid literal for int()" in texto_erro:
                print("\n[AÇÃO INTERROMPIDA]: Digitação inválida. Digite apenas números inteiros sem letras como 'h' ou 'min'.")
            else:
                print(f"\n[AÇÃO INTERROMPIDA]: {erro_val}")
        except Exception as erro:
            print(f"\n[ERRO INESPERADO]: Ocorreu um problema ({erro}).")