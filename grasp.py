import random
from copy import deepcopy

from instancia import Instancia
from solucao import calcular_makespan
from busca_local import busca_2opt


def melhor_insercao(
    instancia: Instancia,
    solucao: list[list[int]],
    cirurgia: int
):
    """
    Encontra a melhor forma de inserir uma cirurgia
    na solução atual.

    Testa todas as salas e todas as posições possíveis.
    Retorna:
        melhor_solucao,
        melhor_makespan
    """

    melhor_solucao = None
    melhor_makespan = float("inf")

    for indice_sala, sala in enumerate(solucao):

        for posicao in range(len(sala) + 1):

            candidato = deepcopy(solucao)

            candidato[indice_sala].insert(
                posicao,
                cirurgia
            )

            # A solução ainda pode estar incompleta.
            # Portanto não usamos calcular_makespan(),
            # que exige todas as cirurgias presentes.

            tempos_salas = []

            for sala_candidata in candidato:
                tempo = 0

                for i, cirurgia_atual in enumerate(sala_candidata):
                    tempo += instancia.tempos[cirurgia_atual]

                    if i > 0:
                        anterior = sala_candidata[i - 1]

                        tempo += instancia.setup[
                            anterior
                        ][cirurgia_atual]

                tempos_salas.append(tempo)

            makespan = max(tempos_salas)

            if makespan < melhor_makespan:
                melhor_makespan = makespan
                melhor_solucao = candidato

    return melhor_solucao, melhor_makespan


def construir_solucao_grasp(
    instancia: Instancia,
    alpha: float = 0.5,
    rng: random.Random | None = None
):
    """
    Fase construtiva do GRASP.

    Para cada cirurgia ainda não alocada:
    - encontra sua melhor inserção;
    - cria uma Lista Restrita de Candidatos (LRC);
    - sorteia um candidato da LRC;
    - insere a cirurgia escolhida.

    alpha = 0 -> totalmente guloso
    alpha = 1 -> totalmente aleatório
    """

    if not 0 <= alpha <= 1:
        raise ValueError("alpha deve estar entre 0 e 1.")

    if rng is None:
        rng = random.Random()

    solucao = [
        [] for _ in range(instancia.num_salas)
    ]

    nao_alocadas = set(
        range(instancia.num_cirurgias)
    )

    while nao_alocadas:

        candidatos = []

        for cirurgia in nao_alocadas:

            solucao_candidata, makespan = melhor_insercao(
                instancia,
                solucao,
                cirurgia
            )

            candidatos.append(
                (
                    cirurgia,
                    makespan,
                    solucao_candidata
                )
            )

        melhor_valor = min(
            candidato[1]
            for candidato in candidatos
        )

        pior_valor = max(
            candidato[1]
            for candidato in candidatos
        )

        limite = (
            melhor_valor
            + alpha * (pior_valor - melhor_valor)
        )

        lrc = [
            candidato
            for candidato in candidatos
            if candidato[1] <= limite
        ]

        escolhido = rng.choice(lrc)

        cirurgia_escolhida = escolhido[0]
        solucao = escolhido[2]

        nao_alocadas.remove(
            cirurgia_escolhida
        )

    return solucao


def grasp_2opt(
    instancia: Instancia,
    iteracoes: int = 100,
    alpha: float = 0.5,
    seed: int | None = None
):
    """
    GRASP completo usando 2-opt como busca local.
    """

    rng = random.Random(seed)

    melhor_solucao = None
    melhor_makespan = float("inf")

    for _ in range(iteracoes):

        solucao_inicial = construir_solucao_grasp(
            instancia,
            alpha=alpha,
            rng=rng
        )

        solucao_local, makespan, _ = busca_2opt(
            instancia,
            solucao_inicial
        )

        if makespan < melhor_makespan:
            melhor_makespan = makespan
            melhor_solucao = solucao_local

    return melhor_solucao, melhor_makespan
  
  
from vns import vns

def grasp_vns(
    instancia: Instancia,
    iteracoes: int = 100,
    alpha: float = 0.5,
    seed: int | None = None
):
    """
    GRASP usando VNS como etapa de refinamento.
    """

    rng = random.Random(seed)

    melhor_solucao = None
    melhor_makespan = float("inf")

    for _ in range(iteracoes):

        solucao_inicial = construir_solucao_grasp(
            instancia,
            alpha=alpha,
            rng=rng
        )

        solucao_local, makespan, _ = vns(
            instancia,
            solucao_inicial,
            seed=rng.randint(
                0,
                1_000_000
            )
        )

        if makespan < melhor_makespan:
            melhor_makespan = makespan
            melhor_solucao = solucao_local

    return melhor_solucao, melhor_makespan