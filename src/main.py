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

sistema = SistemaFocusU()

while True:
    print("\n════════════════════════════")
    print("         FOCUS U 2.0")
    print("════════════════════════════")
    print("1 - Cadastro")
    print("2 - Criar Disciplina Geral")
    print("3 - Vincular Disciplina ao Aluno")
    print("4 - Criar Rotina para Aluno")
    print("5 - Criar Postagem (Geral, Dúvida ou Material)")
    print("6 - Criar Evento")
    print("7 - Listar Alunos e suas Rotinas")
    print("8 - Exibir Feed")
    print("9 - Curtir Postagem")
    print("10 - Comentar Postagem")
    print("11 - Estatísticas")
    print("12 - Apagar Conta")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    try:
        if opcao == "1":
            mat = input("Matrícula: ")
            nome = input("Nome de Usuário: ")
            email = input("Email: ")

            matricula_repetida = False
            nome_repetido = False
            email_repetido = False

            for a in sistema.alunos:
                if a.matricula.strip() == mat.strip():
                    matricula_repetida = True
                    break
                if a.nome.strip().lower() == nome.strip().lower():
                    nome_repetido = True
                    break
                if a.email.strip().lower() == email.strip().lower():
                    email_repetido = True
                    break

            if matricula_repetida:
                print(f"\n[AÇÃO CANCELADA]: A matrícula '{mat}' já está cadastrada!")
                continue

            if nome_repetido:
                print(f"\n[AÇÃO CANCELADA]: O nome de usuário '{nome}' já está em uso!")
                continue

            if email_repetido:
                print(f"\n[AÇÃO CANCELADA]: O e-mail '{email}' já está cadastrado em outra conta!")
                continue

            sistema.adicionar_aluno(Aluno(nome, email, mat))
            print("\nAluno cadastrado com sucesso!")

        elif opcao == "2":
            nome, prof = input("Disciplina: "), input("Professor: ")
            sistema.adicionar_disciplina_global(Disciplina(nome, prof))
            print("\nDisciplina criada no sistema!")

        elif opcao == "3":
            if not sistema.alunos or not sistema.disciplinas_globais:
                print("Cadastre alunos e disciplinas primeiro."); continue

            for i, a in enumerate(sistema.alunos): print(f"{i} - {a.nome}")
            idx_a = int(input("Escolha o aluno: "))
            if idx_a < 0: raise IndexError("Índices negativos não são permitidos.")

            for i, d in enumerate(sistema.disciplinas_globais): print(f"{i} - {d.nome}")
            idx_d = int(input("Escolha a disciplina: "))
            if idx_d < 0: raise IndexError("Índices negativos não são permitidos.")

            sistema.alunos[idx_a].adicionar_disciplina(sistema.disciplinas_globais[idx_d])
            print("\nMatrícula na disciplina efetuada!")

        elif opcao == "4":
            if not sistema.alunos: print("Cadastre um aluno primeiro."); continue
            for i, a in enumerate(sistema.alunos): print(f"{i} - {a.nome}")
            idx = int(input("Escolha o aluno dono da rotina: "))
            if idx < 0: raise IndexError("Índices negativos não são permitidos.")

            atv, temp = input("Atividade: "), int(input("Tempo (min): "))
            sistema.alunos[idx].adicionar_rotina(Rotina(atv, temp))
            print("\nRotina salva no perfil do aluno!")

        elif opcao == "5":
            if not sistema.alunos: print("Cadastre um aluno primeiro."); continue
            for i, a in enumerate(sistema.alunos): print(f"{i} - {a.nome}")
            idx = int(input("Autor: "))
            if idx < 0: raise IndexError("Índices negativos não são permitidos.")

            print("\nTipo: 1-Geral | 2-Dúvida | 3-Material")
            tipo = input("Escolha: ")
            t, c = input("Título: "), input("Conteúdo: ")

            if tipo == "2":
                disc = input("Disciplina da dúvida: ")
                p = PostagemDuvida(t, c, sistema.alunos[idx], disc)
            elif tipo == "3":
                link = input("Link do material: ")
                p = PostagemMaterial(t, c, sistema.alunos[idx], link)
            else:
                p = Postagem(t, c, sistema.alunos[idx])

            sistema.adicionar_postagem(p)
            print("\nPostagem enviada ao feed!")

        elif opcao == "6":
            t, d, h = input("Título: "), input("Data: "), input("Horário: ")
            sistema.adicionar_evento(Evento(t, d, h))
            print("\nEvento publicado!")

        elif opcao == "7": sistema.listar_alunos()
        elif opcao == "8": sistema.exibir_feed()

        elif opcao == "9":
            if not sistema.postagens: print("Nenhum post disponível."); continue
            for i, p in enumerate(sistema.postagens): print(f"{i} - {p.titulo}")
            idx = int(input("Escolha o post: "))
            if idx < 0: raise IndexError("Índices negativos não são permitidos.")
            sistema.postagens[idx].curtir()
            print("\nVocê curtiu essa publicação!")

        elif opcao == "10":
            if not sistema.postagens: print("Nenhum post disponível."); continue
            for i, p in enumerate(sistema.postagens): print(f"{i} - {p.titulo}")
            idx = int(input("Escolha o post: "))
            if idx < 0: raise IndexError("Índices negativos não são permitidos.")
            coment = input("Comentário: ")
            sistema.postagens[idx].comentar(coment)
            print("\nComentário publicado!")

        elif opcao == "11": sistema.estatisticas()

        elif opcao == "12":
            if not sistema.alunos: print("Nenhum aluno no sistema."); continue
            for i, a in enumerate(sistema.alunos): print(f"{i} - {a.nome}")
            idx = int(input("Remover ID: "))
            if idx < 0: raise IndexError("Índices negativos não são permitidos.")
            aluno_alvo = sistema.alunos[idx]
            sistema.remover_aluno(aluno_alvo)
            print(f"\nConta de {aluno_alvo.nome} e suas rotinas foram apagadas!")

        elif opcao == "0": break

    except (ValueError, IndexError) as erro_especifico:
        print(f"\n[AÇÃO INTERRUPTIDA]: Entrada inválida ou operação incorreta. ({erro_especifico})")
    except Exception as erro:
        print(f"\nErro operacional: {erro}")