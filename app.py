import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches


st.set_page_config(
    page_title="Calculadora de Aproveitamento de Papel",
    layout="centered"
)

st.title("M87 • Calculadora de Formatos")


# ==================================================
# PAINEL VISUAL
# ==================================================

linha1_col1, linha1_col2 = st.columns(2)

with linha1_col1:
    papel_largura = st.number_input("Largura do papel (mm)", value=450, min_value=1, key="papel_largura")

with linha1_col2:
    papel_altura = st.number_input("Altura do papel (mm)", value=320, min_value=1, key="papel_altura")


linha2_col1, linha2_col2 = st.columns(2)

with linha2_col1:
    peca_largura = st.number_input("Largura da peça (mm)", value=90, min_value=1, key="peca_largura")

with linha2_col2:
    peca_altura = st.number_input("Altura da peça (mm)", value=50, min_value=1, key="peca_altura")


linha3_col1, linha3_col2 = st.columns(2)

with linha3_col1:
    espaco = st.number_input("Espaço entre peças (mm)", value=5, min_value=0, key="espaco")

with linha3_col2:
    margem = st.number_input("Margem de segurança (mm)", value=5, min_value=0, key="margem")


# ==================================================
# CÁLCULO
# ==================================================

def calcular(papel_l, papel_a, peca_l, peca_a, espaco, margem):
    area_util_l = papel_l - margem * 2
    area_util_a = papel_a - margem * 2

    colunas = int((area_util_l + espaco) // (peca_l + espaco))
    linhas = int((area_util_a + espaco) // (peca_a + espaco))

    colunas = max(0, colunas)
    linhas = max(0, linhas)

    total = colunas * linhas

    largura_ocupada = colunas * peca_l + max(0, colunas - 1) * espaco
    altura_ocupada = linhas * peca_a + max(0, linhas - 1) * espaco

    inicio_x = margem + (area_util_l - largura_ocupada) / 2
    inicio_y = margem + (area_util_a - altura_ocupada) / 2

    return {
        "peca_l": peca_l,
        "peca_a": peca_a,
        "colunas": colunas,
        "linhas": linhas,
        "total": total,
        "inicio_x": inicio_x,
        "inicio_y": inicio_y
    }


def obter_opcoes():
    normal = calcular(
        papel_largura,
        papel_altura,
        peca_largura,
        peca_altura,
        espaco,
        margem
    )
    normal["orientacao"] = "Peça normal"

    rotacionado = calcular(
        papel_largura,
        papel_altura,
        peca_altura,
        peca_largura,
        espaco,
        margem
    )
    rotacionado["orientacao"] = "Peça rotacionada 90°"

    opcoes = [normal, rotacionado]

    return sorted(
        opcoes,
        key=lambda opcao: opcao["total"],
        reverse=True
    )


# ==================================================
# DESENHO
# ==================================================

def desenhar(resultado):
    fig, ax = plt.subplots(figsize=(9, 6))

    # Folha
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            papel_largura,
            papel_altura,
            fill=False,
            linewidth=2,
            edgecolor="black"
        )
    )

    # Margem de segurança
    ax.add_patch(
        patches.Rectangle(
            (margem, margem),
            papel_largura - margem * 2,
            papel_altura - margem * 2,
            fill=False,
            linestyle="--",
            linewidth=0.7,
            edgecolor="0.65"
        )
    )

    # Peças centralizadas
    for linha in range(resultado["linhas"]):
        for coluna in range(resultado["colunas"]):
            x = resultado["inicio_x"] + coluna * (resultado["peca_l"] + espaco)
            y = resultado["inicio_y"] + linha * (resultado["peca_a"] + espaco)

            ax.add_patch(
                patches.Rectangle(
                    (x, y),
                    resultado["peca_l"],
                    resultado["peca_a"],
                    fill=False,
                    linewidth=1,
                    edgecolor="black"
                )
            )

    ax.set_xlim(0, papel_largura)
    ax.set_ylim(0, papel_altura)
    ax.set_aspect("equal")

    ax.set_title(
        f'{resultado["orientacao"]} | '
        f'{resultado["colunas"]} x {resultado["linhas"]} = '
        f'{resultado["total"]} peças',
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig


# ==================================================
# BOTÕES
# ==================================================

opcoes = obter_opcoes()

botao1, botao2 = st.columns(2)

with botao1:
    melhor = st.button("Melhor montagem", type="primary")

with botao2:
    segunda = st.button("Segunda melhor montagem")


if melhor:
    resultado = opcoes[0]

    st.pyplot(desenhar(resultado))

    st.write(f"(largura do papel: {papel_largura} mm)")
    st.write(f"(altura do papel: {papel_altura} mm)")

    st.success(f"Melhor opção: {resultado['orientacao']}")
    st.write(f"Quantidade: **{resultado['total']} peças**")
    st.write(f"Montagem: **{resultado['colunas']} colunas x {resultado['linhas']} linhas**")
    st.write(f"Tamanho usado da peça: **{resultado['peca_l']} x {resultado['peca_a']} mm**")
    st.write(f"Espaço entre peças: **{espaco} mm**")
    st.write(f"Margem de segurança: **{margem} mm**")


if segunda:
    resultado = opcoes[1]

    st.pyplot(desenhar(resultado))

    st.warning(f"Opção exibida: {resultado['orientacao']}")
    st.write(f"(largura do papel: {papel_largura} mm)")
    st.write(f"(altura do papel: {papel_altura} mm)")

    st.write(f"Quantidade: **{resultado['total']} peças**")
    st.write(f"Montagem: **{resultado['colunas']} colunas x {resultado['linhas']} linhas**")
    st.write(f"Tamanho usado da peça: **{resultado['peca_l']} x {resultado['peca_a']} mm**")
    st.write(f"Espaço entre peças: **{espaco} mm**")
    st.write(f"Margem de segurança: **{margem} mm**")