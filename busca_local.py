from copy import deepcopy

from instancia import Instancia
from solucao import calcular_makespan


def busca_2opt(instancia: Instancia, solucao: list[list[int]]):
    """
    Busca local 2-opt adaptada ao POACE.

    Testa a troca de posição entre quaisquer duas cirurgias
    da solução, inclusive entre salas diferentes.

    Em cada rodada, aplica a melhor troca encontrada.
    """

    atual = deepcopy(solucao)
    makespan_atual = calcular_makespan(instancia, atual)

    melhorias = 0

    while True:
        melhor_vizinho = None
        melhor_makespan = makespan_atual

        # Lista com todas as posições ocupadas da solução.
        posicoes = []

        for indice_sala, sala in enumerate(atual):
            for indice_cirurgia in range(len(sala)):
                posicoes.append(
                    (indice_sala, indice_cirurgia)
                )

        # Testa todos os pares de cirurgias.
        for a in range(len(posicoes) - 1):

            sala_a, pos_a = posicoes[a]

            for b in range(a + 1, len(posicoes)):

                sala_b, pos_b = posicoes[b]

                vizinho = deepcopy(atual)

                cirurgia_a = vizinho[sala_a][pos_a]
                cirurgia_b = vizinho[sala_b][pos_b]

                vizinho[sala_a][pos_a] = cirurgia_b
                vizinho[sala_b][pos_b] = cirurgia_a

                makespan = calcular_makespan(
                    instancia,
                    vizinho
                )

                if makespan < melhor_makespan:
                    melhor_makespan = makespan
                    melhor_vizinho = vizinho

        if melhor_vizinho is None:
            break

        atual = melhor_vizinho
        makespan_atual = melhor_makespan
        melhorias += 1

    return atual, makespan_atual, melhorias