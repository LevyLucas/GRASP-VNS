from copy import deepcopy

from instancia import Instancia
from solucao import tempo_sala


def busca_2opt(
    instancia: Instancia,
    solucao: list[list[int]]
):

    atual = deepcopy(solucao)

    tempos_salas = [
        tempo_sala(instancia, sala)
        for sala in atual
    ]

    makespan_atual = max(tempos_salas)

    melhorias = 0

    while True:

        melhor_movimento = None
        melhor_makespan = makespan_atual

        posicoes = []

        for indice_sala, sala in enumerate(atual):
            for indice_cirurgia in range(len(sala)):
                posicoes.append(
                    (
                        indice_sala,
                        indice_cirurgia
                    )
                )

        for a in range(len(posicoes) - 1):

            sala_a, pos_a = posicoes[a]

            for b in range(a + 1, len(posicoes)):

                sala_b, pos_b = posicoes[b]

                # Faz a troca temporariamente.
                atual[sala_a][pos_a], atual[sala_b][pos_b] = (
                    atual[sala_b][pos_b],
                    atual[sala_a][pos_a]
                )

                if sala_a == sala_b:

                    novo_tempo_a = tempo_sala(
                        instancia,
                        atual[sala_a]
                    )

                    tempos_candidatos = tempos_salas.copy()

                    tempos_candidatos[sala_a] = novo_tempo_a

                else:

                    novo_tempo_a = tempo_sala(
                        instancia,
                        atual[sala_a]
                    )

                    novo_tempo_b = tempo_sala(
                        instancia,
                        atual[sala_b]
                    )

                    tempos_candidatos = tempos_salas.copy()

                    tempos_candidatos[sala_a] = novo_tempo_a
                    tempos_candidatos[sala_b] = novo_tempo_b

                makespan = max(
                    tempos_candidatos
                )

                # Desfaz a troca.
                atual[sala_a][pos_a], atual[sala_b][pos_b] = (
                    atual[sala_b][pos_b],
                    atual[sala_a][pos_a]
                )

                if makespan < melhor_makespan:

                    melhor_makespan = makespan

                    melhor_movimento = (
                        sala_a,
                        pos_a,
                        sala_b,
                        pos_b
                    )

        if melhor_movimento is None:
            break

        sala_a, pos_a, sala_b, pos_b = melhor_movimento

        atual[sala_a][pos_a], atual[sala_b][pos_b] = (
            atual[sala_b][pos_b],
            atual[sala_a][pos_a]
        )

        tempos_salas[sala_a] = tempo_sala(
            instancia,
            atual[sala_a]
        )

        if sala_a != sala_b:

            tempos_salas[sala_b] = tempo_sala(
                instancia,
                atual[sala_b]
            )

        makespan_atual = max(
            tempos_salas
        )

        melhorias += 1

    return (
        atual,
        makespan_atual,
        melhorias
    )
