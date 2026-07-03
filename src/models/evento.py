from interfaces.publicavel import Publicavel

class Evento(Publicavel):
    total_eventos = 0

    def __init__(self, titulo, data, horario):
        self.titulo = titulo
        self.data = data
        self.horario = horario
        Evento.total_eventos += 1

    def __del__(self):
        if Evento.total_eventos > 0:
            Evento.total_eventos -= 1

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor.strip():
            raise ValueError("Título inválido.")
        self._titulo = valor

    # Implementação do método do contrato
    def publicar(self):
        return (
            f"\n[EVENTO ACADÊMICO]\n"
            f"Título: {self.titulo}\n"
            f"Data: {self.data}\n"
            f"Horário: {self.horario}"
        )
