class Rotina:
    total_rotinas = 0
    def __init__(self, atividade, tempo):
        self._atividade = atividade
        self.tempo = tempo
        Rotina.total_rotinas += 1
    def __del__(self):
        if Rotina.total_rotinas > 0: Rotina.total_rotinas -= 1
    @property
    def atividade(self): return self._atividade
    @atividade.setter
    def atividade(self, valor):
        if not valor.strip(): raise ValueError("Atividade inválida.")
        self._atividade = valor
    @property
    def tempo(self): return self._tempo
    @tempo.setter
    def tempo(self, valor):
        if valor <= 0: raise ValueError("Tempo deve ser maior que zero.")
        self._tempo = valor
    def __str__(self): return f"{self.atividade} | {self.tempo} min"