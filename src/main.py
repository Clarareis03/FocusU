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

# Conjunto com as opções válidas do menu para validação rápida O(1)
OPCOES_VALIDAS = {str(i) for i in range(13)}  # '0' até '12'

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

    opcao = input("\nEscolha uma opção: ").strip()

    # BLINDAGEM 1: Trata entradas que não estão no menu (ex: "abc", "99", "")
    if opcao not in OPCOES_VALIDAS:
        print("\n[OPÇÃO INVÁLIDA]: Por favor, digite apenas um número de 0 a 12 de acordo com o menu.")
        continue

    try:
        if opcao == "1":
            mat = input("Matrícula: ").strip()
            nome = input("Nome de Usuário: ").strip()
            email = input("Email: ").strip()

            if not mat or not nome or not email:
                print("\n[AÇÃO CANCELADA]: Todos os campos devem ser preenchidos.")
                continue

            sistema.adicionar_aluno(Aluno(nome, email, mat))
            print("\nAluno cadastrado com sucesso!")

        elif opcao == "2":
            nome = input("Disciplina: ").strip()
            prof = input("Professor: ").strip()

            if not nome or not prof:
                print("\n[AÇÃO CANCELADA]: Todos os campos devem ser preenchidos.")
                continue

            sistema.adicionar_disciplina_global(Disciplina(nome, prof))
            print("\nDisciplina criada no sistema!")

        elif opcao == "3":
            lista_alunos = list(sistema.alunos_por_matricula.values())
            lista_disciplinas = list(sistema.disciplinas_por_nome.values())

            if not lista_alunos or not lista_disciplinas:
                print("Cadastre alunos e disciplinas primeiro."); continue

            for i, a in enumerate(lista_alunos): print(f"{i} - {a.nome}")
            idx_a = int(input("Escolha o aluno (número): "))
            if idx_a < 0 or idx_a >= len(lista_alunos):
                raise IndexError("Índice de aluno fora da lista.")

            for i, d in enumerate(lista_disciplinas): print(f"{i} - {d.nome}")
            idx_d = int(input("Escolha a disciplina (número): "))
            if idx_d < 0 or idx_d >= len(lista_disciplinas):
                raise IndexError("Índice de disciplina fora da lista.")

            lista_alunos[idx_a].adicionar_disciplina(lista_disciplinas[idx_d])
            print("\nMatrícula na disciplina efetuada!")

        elif opcao == "4":
            lista_alunos = list(sistema.alunos_por_matricula.values())
            if not lista_alunos: print("Cadastre um aluno primeiro."); continue

            for i, a in enumerate(lista_alunos): print(f"{i} - {a.nome}")
            idx = int(input("Escolha o aluno dono da rotina (número): "))
            if idx < 0 or idx >= len(lista_alunos):
                raise IndexError("Índice de aluno fora da lista.")

            atv = input("Atividade: ").strip()
            temp = int(input("Tempo em minutos: "))
            
            if temp <= 0:
                print("\n[AÇÃO CANCELADA]: O tempo deve ser maior que 0.")
                continue

            lista_alunos[idx].adicionar_rotina(Rotina(atv, temp))
            print("\nRotina salva no perfil do aluno!")

        elif opcao == "5":
            lista_alunos = list(sistema.alunos_por_matricula.values())
            if not lista_alunos: print("Cadastre um aluno primeiro."); continue

            for i, a in enumerate(lista_alunos): print(f"{i} - {a.nome}")
            idx = int(input("Autor (número): "))
            if idx < 0 or idx >= len(lista_alunos):
                raise IndexError("Índice de autor fora da lista.")

            print("\nTipo: 1-Geral | 2-Dúvida | 3-Material")
            tipo = input("Escolha: ").strip()
            t, c = input("Título: ").strip(), input("Conteúdo: ").strip()

            if tipo == "2":
                disc = input("Disciplina da dúvida: ").strip()
                p = PostagemDuvida(t, c, lista_alunos[idx], disc)
            elif tipo == "3":
                link = input("Link do material: ").strip()
                p = PostagemMaterial(t, c, lista_alunos[idx], link)
            else:
                p = Postagem(t, c, lista_alunos[idx])

            sistema.adicionar_postagem(p)
            print("\nPostagem enviada ao feed!")

        elif opcao == "6":
            t, d, h = input("Título: ").strip(), input("Data: ").strip(), input("Horário: ").strip()
            sistema.adicionar_evento(Evento(t, d, h))
            print("\nEvento publicado!")

        elif opcao == "7": sistema.listar_alunos()
        elif opcao == "8": sistema.exibir_feed()

        elif opcao == "9":
            if not sistema.postagens: print("Nenhum post disponível."); continue
            for i, p in enumerate(sistema.postagens): print(f"{i} - {p.titulo}")
            idx = int(input("Escolha o post (número): "))
            if idx < 0 or idx >= len(sistema.postagens):
                raise IndexError("Índice de post fora da lista.")
            sistema.postagens[idx].curtir()
            print("\nVocê curtiu essa publicação!")

        elif opcao == "10":
            if not sistema.postagens: print("Nenhum post disponível."); continue
            for i, p in enumerate(sistema.postagens): print(f"{i} - {p.titulo}")
            idx = int(input("Escolha o post (número): "))
            if idx < 0 or idx >= len(sistema.postagens):
                raise IndexError("Índice de post fora da lista.")
            coment = input("Comentário: ").strip()
            sistema.postagens[idx].comentar(coment)
            print("\nComentário publicado!")

        elif opcao == "11": sistema.estatisticas()

        elif opcao == "12":
            lista_alunos = list(sistema.alunos_por_matricula.values())
            if not lista_alunos: print("Nenhum aluno no sistema."); continue

            for i, a in enumerate(lista_alunos): print(f"{i} - {a.nome}")
            idx = int(input("Remover ID (número): "))
            if idx < 0 or idx >= len(lista_alunos):
                raise IndexError("Índice fora da lista.")
            aluno_alvo = lista_alunos[idx]
            sistema.remover_aluno(aluno_alvo)
            print(f"\nConta de {aluno_alvo.nome} e suas rotinas foram apagadas!")

        elif opcao == "0":
            print("\nSaindo do Focus U... Até logo!")
            break

    # BLINDAGEM 2: Captura qualquer erro de tipo ou índice inválido
    except ValueError as erro_val:
        print(f"\n[AÇÃO INTERRUPTIDA]: Digitação inválida. Esperava-se um número/valor correto. ({erro_val})")
    except IndexError as erro_idx:
        print(f"\n[AÇÃO INTERRUPTIDA]: O número escolhido não está na lista. ({erro_idx})")
    except Exception as erro:
        print(f"\nErro operacional inesperado: {erro}")