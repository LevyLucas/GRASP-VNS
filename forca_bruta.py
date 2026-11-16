from itertools import permutations

from instancia import Instancia
from solucao import calcular_makespan


def gerar_distribuicoes(total, partes):
    """
    Gera todas as formas de dividir 'total' cirurgias
    entre 'partes' salas.

    Exemplo:
    total = 4
    partes = 2

    Pode gerar:
    (0, 4)
    (1, 3)
    (2, 2)
    (3, 1)
    (4, 0)
    """

    if partes == 1:
        yield (total,)
        return

    for quantidade in range(total + 1):
        for restante in gerar_distribuicoes(
            total - quantidade,
            partes - 1
        ):
            yield (quantidade,) + restante


def forca_bruta(instancia: Instancia):
    cirurgias = list(range(instancia.num_cirurgias))

    melhor_solucao = None
    melhor_makespan = float("inf")

    distribuicoes = list(
        gerar_distribuicoes(
            instancia.num_cirurgias,
            instancia.num_salas
        )
    )

    for ordem in permutations(cirurgias):

        for distribuicao in distribuicoes:

            solucao = []
            inicio = 0

            for quantidade in distribuicao:
                fim = inicio + quantidade

                sala = list(ordem[inicio:fim])
                solucao.append(sala)

                inicio = fim

            makespan = calcular_makespan(
                instancia,
                solucao
            )

            if makespan < melhor_makespan:
                melhor_makespan = makespan
                melhor_solucao = solucao

    return melhor_solucao, melhor_makespan