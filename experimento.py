import csv
import os
import statistics
import time

from instancia import carregar_instancia
from grasp import grasp_2opt, grasp_vns


EXECUCOES = 10
ITERACOES_GRASP = 50
ALPHA = 0.5

INSTANCIAS = [
    "SINT-11-S3",
    "SINT-21-S2",
    "SINT-50-S4",
    "SINT-75-S5",
]


def executar_metodo(
    nome_metodo,
    funcao,
    instancia,
    seed
):
    inicio = time.perf_counter()

    _, makespan = funcao(
        instancia,
        iteracoes=ITERACOES_GRASP,
        alpha=ALPHA,
        seed=seed
    )

    tempo = time.perf_counter() - inicio

    return {
        "metodo": nome_metodo,
        "makespan": makespan,
        "tempo": tempo
    }


def salvar_resultados_detalhados(
    resultados,
    mostrar=False
):
    caminho = (
        "resultados/"
        "resultados_detalhados.csv"
    )

    with open(
        caminho,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "instancia",
            "num_cirurgias",
            "num_salas",
            "execucao",
            "seed",
            "metodo",
            "iteracoes_grasp",
            "alpha",
            "makespan",
            "tempo"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(resultados)

    if mostrar:
        print(
            f"Resultados detalhados salvos em: "
            f"{caminho}"
        )


def gerar_resumo(resultados):
    caminho = (
        "resultados/"
        "resumo.csv"
    )

    resumo = []

    for nome_instancia in INSTANCIAS:

        for metodo in [
            "GRASP+2-opt",
            "GRASP+VNS"
        ]:

            dados = [
                resultado
                for resultado in resultados
                if resultado["instancia"] == nome_instancia
                and resultado["metodo"] == metodo
            ]

            if not dados:
                continue

            makespans = [
                resultado["makespan"]
                for resultado in dados
            ]

            tempos = [
                resultado["tempo"]
                for resultado in dados
            ]

            if len(makespans) > 1:
                desvio = statistics.stdev(
                    makespans
                )
            else:
                desvio = 0.0

            resumo.append({
                "instancia":
                    nome_instancia,

                "metodo":
                    metodo,

                "melhor_makespan":
                    min(makespans),

                "media_makespan":
                    statistics.mean(makespans),

                "desvio_makespan":
                    desvio,

                "pior_makespan":
                    max(makespans),

                "tempo_medio":
                    statistics.mean(tempos),

                "melhor_tempo":
                    min(tempos),

                "pior_tempo":
                    max(tempos)
            })

    with open(
        caminho,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "instancia",
            "metodo",
            "melhor_makespan",
            "media_makespan",
            "desvio_makespan",
            "pior_makespan",
            "tempo_medio",
            "melhor_tempo",
            "pior_tempo"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(resumo)

    print(
        f"Resumo salvo em: {caminho}"
    )

    return resumo


def gerar_comparacao(resultados):
    caminho = (
        "resultados/"
        "comparacao.csv"
    )

    comparacoes = []

    for nome_instancia in INSTANCIAS:

        dados_2opt = {
            resultado["execucao"]: resultado
            for resultado in resultados
            if resultado["instancia"] == nome_instancia
            and resultado["metodo"] == "GRASP+2-opt"
        }

        dados_vns = {
            resultado["execucao"]: resultado
            for resultado in resultados
            if resultado["instancia"] == nome_instancia
            and resultado["metodo"] == "GRASP+VNS"
        }

        execucoes = sorted(
            set(dados_2opt)
            & set(dados_vns)
        )

        if not execucoes:
            continue

        vitorias_vns = 0
        empates = 0
        derrotas_vns = 0

        melhorias_percentuais = []

        for execucao in execucoes:

            makespan_2opt = (
                dados_2opt[execucao]["makespan"]
            )

            makespan_vns = (
                dados_vns[execucao]["makespan"]
            )

            if makespan_vns < makespan_2opt:
                vitorias_vns += 1

            elif makespan_vns == makespan_2opt:
                empates += 1

            else:
                derrotas_vns += 1

            melhoria = (
                (
                    makespan_2opt
                    - makespan_vns
                )
                / makespan_2opt
                * 100
            )

            melhorias_percentuais.append(
                melhoria
            )

        tempo_2opt = statistics.mean(
            dados_2opt[execucao]["tempo"]
            for execucao in execucoes
        )

        tempo_vns = statistics.mean(
            dados_vns[execucao]["tempo"]
            for execucao in execucoes
        )

        comparacoes.append({
            "instancia":
                nome_instancia,

            "vitorias_vns":
                vitorias_vns,

            "empates":
                empates,

            "derrotas_vns":
                derrotas_vns,

            "melhoria_media_percentual":
                statistics.mean(
                    melhorias_percentuais
                ),

            "razao_tempo_vns_2opt":
                tempo_vns / tempo_2opt
        })

    with open(
        caminho,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "instancia",
            "vitorias_vns",
            "empates",
            "derrotas_vns",
            "melhoria_media_percentual",
            "razao_tempo_vns_2opt"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(comparacoes)

    print(
        f"Comparação salva em: {caminho}"
    )

    return comparacoes


def main():
    os.makedirs(
        "resultados",
        exist_ok=True
    )

    resultados = []

    for nome_instancia in INSTANCIAS:

        print()
        print("=" * 60)
        print(
            f"Instância: {nome_instancia}"
        )
        print("=" * 60)

        instancia = carregar_instancia(
            f"instancias/{nome_instancia}.json"
        )

        for execucao in range(
            1,
            EXECUCOES + 1
        ):

            # Mesma seed para os dois métodos.
            seed = 1000 + execucao

            print(
                f"\nExecução "
                f"{execucao}/{EXECUCOES}"
            )

            resultado_2opt = executar_metodo(
                "GRASP+2-opt",
                grasp_2opt,
                instancia,
                seed
            )

            resultados.append({
                "instancia":
                    nome_instancia,

                "num_cirurgias":
                    instancia.num_cirurgias,

                "num_salas":
                    instancia.num_salas,

                "execucao":
                    execucao,

                "seed":
                    seed,

                "iteracoes_grasp":
                    ITERACOES_GRASP,

                "alpha":
                    ALPHA,

                **resultado_2opt
            })

            print(
                f"  GRASP+2-opt -> "
                f"makespan = "
                f"{resultado_2opt['makespan']} | "
                f"tempo = "
                f"{resultado_2opt['tempo']:.4f}s"
            )

            resultado_vns = executar_metodo(
                "GRASP+VNS",
                grasp_vns,
                instancia,
                seed
            )

            resultados.append({
                "instancia":
                    nome_instancia,

                "num_cirurgias":
                    instancia.num_cirurgias,

                "num_salas":
                    instancia.num_salas,

                "execucao":
                    execucao,

                "seed":
                    seed,

                "iteracoes_grasp":
                    ITERACOES_GRASP,

                "alpha":
                    ALPHA,

                **resultado_vns
            })

            print(
                f"  GRASP+VNS   -> "
                f"makespan = "
                f"{resultado_vns['makespan']} | "
                f"tempo = "
                f"{resultado_vns['tempo']:.4f}s"
            )
            salvar_resultados_detalhados(
                resultados
            )

    print()

    salvar_resultados_detalhados(
        resultados,
        mostrar=True
    )

    resumo = gerar_resumo(
        resultados
    )

    comparacoes = gerar_comparacao(
        resultados
    )

    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)

    for linha in resumo:

        print(
            f"{linha['instancia']:12} | "
            f"{linha['metodo']:12} | "
            f"melhor = "
            f"{linha['melhor_makespan']:6.0f} | "
            f"média = "
            f"{linha['media_makespan']:8.2f} | "
            f"desvio = "
            f"{linha['desvio_makespan']:7.2f} | "
            f"tempo = "
            f"{linha['tempo_medio']:8.4f}s"
        )

    print()
    print("=" * 60)
    print("COMPARAÇÃO PAREADA")
    print("=" * 60)

    for linha in comparacoes:

        print(
            f"{linha['instancia']:12} | "
            f"V/E/D = "
            f"{linha['vitorias_vns']}/"
            f"{linha['empates']}/"
            f"{linha['derrotas_vns']} | "
            f"melhoria média = "
            f"{linha['melhoria_media_percentual']:.3f}% | "
            f"tempo VNS/2-opt = "
            f"{linha['razao_tempo_vns_2opt']:.2f}x"
        )


if __name__ == "__main__":
    main()