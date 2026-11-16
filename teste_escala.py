import time

from instancia import carregar_instancia
from grasp import grasp_2opt, grasp_vns


INSTANCIAS = [
    "SINT-75-S5",
    "SINT-100-S5",
    "SINT-130-S10",
    "SINT-200-S10"
]

ITERACOES = 50
ALPHA = 0.5
SEED = 42


for nome in INSTANCIAS:

    print()
    print("=" * 60)
    print(nome)
    print("=" * 60)

    instancia = carregar_instancia(
        f"instancias/{nome}.json"
    )

    # GRASP + 2-opt
    inicio = time.perf_counter()

    _, makespan_2opt = grasp_2opt(
        instancia,
        iteracoes=ITERACOES,
        alpha=ALPHA,
        seed=SEED
    )

    tempo_2opt = time.perf_counter() - inicio

    print(
        f"GRASP+2-opt -> "
        f"makespan = {makespan_2opt} | "
        f"tempo = {tempo_2opt:.4f}s"
    )

    # GRASP + VNS
    inicio = time.perf_counter()

    _, makespan_vns = grasp_vns(
        instancia,
        iteracoes=ITERACOES,
        alpha=ALPHA,
        seed=SEED
    )

    tempo_vns = time.perf_counter() - inicio

    print(
        f"GRASP+VNS   -> "
        f"makespan = {makespan_vns} | "
        f"tempo = {tempo_vns:.4f}s"
    )

    diferenca = makespan_2opt - makespan_vns

    print(
        f"Diferença   -> {diferenca}"
    )