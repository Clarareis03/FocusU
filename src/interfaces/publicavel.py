# CONCEITO: INTERFACE
# Define um contrato de comportamento obrigatório para o Feed.
from abc import ABC, abstractmethod

class Publicavel(ABC):
    @abstractmethod
    def publicar(self):
        pass
