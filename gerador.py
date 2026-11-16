import json
import os
import random


def gerar_instancia(
    nome: str,
    num_cirurgias: int,
    num_salas: int,
    seed: int
):
    rng = random.Random(seed)

    # Duração das cirurgias:
    # valores inteiros entre 30 e 180 minutos.
    tempos = [
        rng.randint(30, 180)
        for _ in range(num_cirurgias)
    ]

    # Matriz de setup:
    # tempo de preparação entre duas cirurgias.
    # Valores entre 5 e 30 minutos.
    setup = []

    for i in range(num_cirurgias):
        linha = []

        for j in range(num_cirurgias):

            if i == j:
                linha.append(0)
            else:
                linha.append(
                    rng.randint(5, 30)
                )

        setup.append(linha)

    instancia = {
        "nome": nome,
        "num_cirurgias": num_cirurgias,
        "num_salas": num_salas,
        "seed": seed,
        "tempos": tempos,
        "setup": setup
    }

    return instancia


def salvar_instancia(instancia, pasta="instancias"):
    os.makedirs(
        pasta,
        exist_ok=True
    )

    caminho = os.path.join(
        pasta,
        f"{instancia['nome']}.json"
    )

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            instancia,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Instância salva: {caminho}"
    )


def main():
    configuracoes = [
        ("SINT-11-S3", 11, 3, 101),
        ("SINT-21-S2", 21, 2, 102),
        ("SINT-50-S4", 50, 4, 103),
        ("SINT-75-S5", 75, 5, 104),
        ("SINT-100-S5", 100, 5, 105),
        ("SINT-130-S10", 130, 10, 106),
        ("SINT-200-S10", 200, 10, 107)
    ]

    for (
        nome,
        num_cirurgias,
        num_salas,
        seed
    ) in configuracoes:

        instancia = gerar_instancia(
            nome=nome,
            num_cirurgias=num_cirurgias,
            num_salas=num_salas,
            seed=seed
        )

        salvar_instancia(
            instancia
        )


if __name__ == "__main__":
    main()