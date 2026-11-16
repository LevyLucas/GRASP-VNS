from instancia import Instancia


def validar_solucao(instancia: Instancia, solucao: list[list[int]]):
    if len(solucao) != instancia.num_salas:
        return False

    cirurgias = []

    for sala in solucao:
        cirurgias.extend(sala)

    if len(cirurgias) != instancia.num_cirurgias:
        return False

    if sorted(cirurgias) != list(range(instancia.num_cirurgias)):
        return False

    return True


def tempo_sala(instancia: Instancia, sala: list[int]):
    if len(sala) == 0:
        return 0

    tempo = 0

    for i, cirurgia in enumerate(sala):
        tempo += instancia.tempos[cirurgia]

        if i > 0:
            cirurgia_anterior = sala[i - 1]
            tempo += instancia.setup[cirurgia_anterior][cirurgia]

    return tempo


def calcular_makespan(instancia: Instancia, solucao: list[list[int]]):
    if not validar_solucao(instancia, solucao):
        raise ValueError("Solução inválida.")

    tempos = []

    for sala in solucao:
        tempos.append(tempo_sala(instancia, sala))

    return max(tempos)