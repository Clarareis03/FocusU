from interfaces.publicavel import Publicavel

# CONCEITO: IMPLEMENTAÇÃO DE INTERFACE
# Classe Postagem assina e implementa o contrato de Publicavel.

class Postagem(Publicavel):
    total_postagens = 0

    def __init__(self, titulo, conteudo, autor):
        self.titulo = titulo
        self.conteudo = conteudo
        self.autor = autor
        self.curtidas = 0
        self.comentarios = []
        Postagem.total_postagens += 1

    def __del__(self):
        if Postagem.total_postagens > 0:
            Postagem.total_postagens -= 1

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor.strip():
            raise ValueError("Título não pode ser vazio.")
        self._titulo = valor

    @property
    def conteudo(self):
        return self._conteudo

    @conteudo.setter
    def conteudo(self, valor):
        if not valor.strip():
            raise ValueError("Conteúdo não pode ser vazio.")
        self._conteudo = valor

    def curtir(self):
        self.curtidas += 1

    def comentar(self, comentario):
        self.comentarios.append(comentario)

    def publicar(self):
        nome_autor = self.autor.nome if self.autor else "Usuário Anônimo"
        return (
            f"\n[POST GERAL]\n"
            f"Título: {self.titulo}\n"
            f"Autor: {nome_autor}\n"
            f"Conteúdo: {self.conteudo}\n"
            f"Curtidas: {self.curtidas} | Comentários: {len(self.comentarios)}"
        )


# CONCEITO: HERANÇA E POLIMORFISMO
# Especializações de Postagem que alteram o método publicar().

class PostagemDuvida(Postagem):
    def __init__(self, titulo, conteudo, autor, disciplina):
        super().__init__(titulo, conteudo, autor)
        self.disciplina = disciplina
        self.resolvida = False

    # Sobrescrita Polimórfica: adiciona status e metadados específicos
    def publicar(self):
        nome_autor = self.autor.nome if self.autor else "Usuário Anônimo"
        status = "[RESOLVIDA]" if self.resolvida else "[ABERTA]"
        return (
            f"\n[DÚVIDA - {self.disciplina.upper()}] {status}\n"
            f"Título: {self.titulo}\n"
            f"Autor: {nome_autor}\n"
            f"Conteúdo: {self.conteudo}\n"
            f"Curtidas: {self.curtidas} | Comentários: {len(self.comentarios)}"
        )


class PostagemMaterial(Postagem):
    def __init__(self, titulo, conteudo, autor, link_download):
        super().__init__(titulo, conteudo, autor)
        self.link_download = link_download

    # Sobrescrita Polimórfica: inclui link de download na visualização
    def publicar(self):
        nome_autor = self.autor.nome if self.autor else "Usuário Anônimo"
        return (
            f"\n[MATERIAL COMPARTILHADO]\n"
            f"Título: {self.titulo}\n"
            f"Autor: {nome_autor}\n"
            f"Conteúdo: {self.conteudo}\n"
            f"Link de Download: {self.link_download}\n"
            f"Curtidas: {self.curtidas} | Comentários: {len(self.comentarios)}"
        )
