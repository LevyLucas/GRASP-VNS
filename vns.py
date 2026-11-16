import random
from copy import deepcopy

from instancia import Instancia
from solucao import calcular_makespan
from busca_local import busca_2opt


def vizinhanca_n1(solucao, rng):
    """
    N1:
    troca duas cirurgias dentro da mesma sala.
    """

    vizinho = deepcopy(solucao)

    salas_validas = [
        i for i, sala in enumerate(vizinho)
        if len(sala) >= 2
    ]

    if not salas_validas:
        return vizinho

    indice_sala = rng.choice(salas_validas)

    i, j = rng.sample(
        range(len(vizinho[indice_sala])),
        2
    )

    vizinho[indice_sala][i], vizinho[indice_sala][j] = (
        vizinho[indice_sala][j],
        vizinho[indice_sala][i]
    )

    return vizinho


def vizinhanca_n2(solucao, rng):
    """
    N2:
    realoca uma cirurgia de uma sala para outra.
    """

    vizinho = deepcopy(solucao)

    salas_origem = [
        i for i, sala in enumerate(vizinho)
        if len(sala) > 0
    ]

    if len(vizinho) < 2 or not salas_origem:
        return vizinho

    origem = rng.choice(salas_origem)

    destinos = [
        i for i in range(len(vizinho))
        if i != origem
    ]

    destino = rng.choice(destinos)

    pos_origem = rng.randrange(
        len(vizinho[origem])
    )

    cirurgia = vizinho[origem].pop(
        pos_origem
    )

    pos_destino = rng.randrange(
        len(vizinho[destino]) + 1
    )

    vizinho[destino].insert(
        pos_destino,
        cirurgia
    )

    return vizinho


def vizinhanca_n3(solucao, rng):
    """
    N3:
    troca uma cirurgia entre duas salas diferentes.
    """

    vizinho = deepcopy(solucao)

    salas_validas = [
        i for i, sala in enumerate(vizinho)
        if len(sala) > 0
    ]

    if len(salas_validas) < 2:
        return vizinho

    sala_a, sala_b = rng.sample(
        salas_validas,
        2
    )

    pos_a = rng.randrange(
        len(vizinho[sala_a])
    )

    pos_b = rng.randrange(
        len(vizinho[sala_b])
    )

    vizinho[sala_a][pos_a], vizinho[sala_b][pos_b] = (
        vizinho[sala_b][pos_b],
        vizinho[sala_a][pos_a]
    )

    return vizinho


def perturbar(solucao, k, rng):
    """
    Aplica o shaking correspondente à vizinhança k.
    """

    if k == 1:
        return vizinhanca_n1(
            solucao,
            rng
        )

    if k == 2:
        return vizinhanca_n2(
            solucao,
            rng
        )

    if k == 3:
        return vizinhanca_n3(
            solucao,
            rng
        )

    raise ValueError(
        f"Vizinhança inválida: {k}"
    )


def vns(
    instancia: Instancia,
    solucao_inicial,
    seed=None
):
    """
    Variable Neighborhood Search.

    N1 -> troca dentro da sala
    N2 -> realocação entre salas
    N3 -> troca entre salas

    Após o shaking, aplica a busca local 2-opt.

    Se melhorar:
        aceita a solução e volta para N1.

    Caso contrário:
        avança para a próxima vizinhança.
    """

    rng = random.Random(seed)

    atual = deepcopy(
        solucao_inicial
    )

    makespan_atual = calcular_makespan(
        instancia,
        atual
    )

    k = 1

    melhorias = 0

    while k <= 3:

        # Shaking
        perturbada = perturbar(
            atual,
            k,
            rng
        )

        # Busca local
        refinada, makespan_refinado, _ = busca_2opt(
            instancia,
            perturbada
        )

        if makespan_refinado < makespan_atual:

            atual = refinada
            makespan_atual = makespan_refinado

            melhorias += 1

            # Encontrou melhora:
            # volta para a primeira vizinhança.
            k = 1

        else:

            # Não melhorou:
            # tenta uma vizinhança mais distante.
            k += 1

    return atual, makespan_atual, melhorias