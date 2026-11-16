from dataclasses import dataclass


@dataclass
class Instancia:
    num_salas: int
    tempos: list[int]
    setup: list[list[int]]

    def __post_init__(self):
        n = len(self.tempos)

        if len(self.setup) != n:
            raise ValueError("A matriz de setup deve ter uma linha por cirurgia.")

        for linha in self.setup:
            if len(linha) != n:
                raise ValueError("A matriz de setup deve ser quadrada.")

    @property
    def num_cirurgias(self):
        return len(self.tempos)