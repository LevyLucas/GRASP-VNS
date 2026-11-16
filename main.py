from instancia import Instancia
from solucao import tempo_sala, calcular_makespan
from forca_bruta import forca_bruta
from busca_local import busca_2opt
from grasp import (
    construir_solucao_grasp,
    grasp_2opt,
    grasp_vns
)


instancia = Instancia(
    num_salas=2,

    tempos=[
        4,
        6,
        3,
        5,
        7
    ],

    setup=[
        [0, 6, 1, 2, 3],
        [2, 0, 6, 1, 2],
        [1, 1, 0, 2, 2],
        [2, 1, 2, 0, 1],
        [3, 2, 2, 1, 0]
    ]
)


# ==========================================================
# SOLUÇÃO MANUAL
# ==========================================================

solucao_inicial = [
    [0, 1, 2],
    [3, 4]
]

print("--- Solução manual ---")

print("Solução:", solucao_inicial)

for i, sala in enumerate(solucao_inicial):
    print(
        f"Sala {i + 1}: {sala} -> tempo = "
        f"{tempo_sala(instancia, sala)}"
    )

print(
    "Makespan:",
    calcular_makespan(
        instancia,
        solucao_inicial
    )
)


# ==========================================================
# BUSCA LOCAL 2-OPT
# ==========================================================

print("\n--- Busca local 2-opt ---")

solucao_2opt, makespan_2opt, melhorias = busca_2opt(
    instancia,
    solucao_inicial
)

print("Solução:", solucao_2opt)

for i, sala in enumerate(solucao_2opt):
    print(
        f"Sala {i + 1}: {sala} -> tempo = "
        f"{tempo_sala(instancia, sala)}"
    )

print("Makespan:", makespan_2opt)
print("Melhorias:", melhorias)


# ==========================================================
# CONSTRUÇÃO GRASP
# ==========================================================

print("\n--- Construção GRASP ---")

solucao_grasp = construir_solucao_grasp(
    instancia,
    alpha=0.5
)

print("Solução:", solucao_grasp)

for i, sala in enumerate(solucao_grasp):
    print(
        f"Sala {i + 1}: {sala} -> tempo = "
        f"{tempo_sala(instancia, sala)}"
    )

print(
    "Makespan:",
    calcular_makespan(
        instancia,
        solucao_grasp
    )
)


# ==========================================================
# GRASP + 2-OPT
# ==========================================================

print("\n--- GRASP + 2-opt ---")

melhor_grasp, makespan_grasp = grasp_2opt(
    instancia,
    iteracoes=100,
    alpha=0.5,
    seed=42
)

print("Melhor solução:", melhor_grasp)

for i, sala in enumerate(melhor_grasp):
    print(
        f"Sala {i + 1}: {sala} -> tempo = "
        f"{tempo_sala(instancia, sala)}"
    )

print(
    "Melhor makespan:",
    makespan_grasp
)


# ==========================================================
# GRASP + VNS
# ==========================================================

print("\n--- GRASP + VNS ---")

melhor_vns, makespan_vns = grasp_vns(
    instancia,
    iteracoes=100,
    alpha=0.5,
    seed=42
)

print("Melhor solução:", melhor_vns)

for i, sala in enumerate(melhor_vns):
    print(
        f"Sala {i + 1}: {sala} -> tempo = "
        f"{tempo_sala(instancia, sala)}"
    )

print(
    "Melhor makespan:",
    makespan_vns
)


# ==========================================================
# FORÇA BRUTA / ÓTIMO
# ==========================================================

print("\n--- Força bruta ---")

solucao_otima, makespan_otimo = forca_bruta(
    instancia
)

print("Solução ótima:", solucao_otima)

for i, sala in enumerate(solucao_otima):
    print(
        f"Sala {i + 1}: {sala} -> tempo = "
        f"{tempo_sala(instancia, sala)}"
    )

print(
    "Makespan ótimo:",
    makespan_otimo
)


# ==========================================================
# COMPARAÇÃO FINAL
# ==========================================================

print("\n--- Comparação ---")

print(
    f"Solução manual:   "
    f"{calcular_makespan(instancia, solucao_inicial)}"
)

print(
    f"2-opt:            "
    f"{makespan_2opt}"
)

print(
    f"GRASP + 2-opt:    "
    f"{makespan_grasp}"
)

print(
    f"GRASP + VNS:      "
    f"{makespan_vns}"
)

print(
    f"Ótimo:            "
    f"{makespan_otimo}"
)