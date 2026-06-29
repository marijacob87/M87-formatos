import math

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import streamlit as st

from core.components import card, titulo_tool
from core.utils import converter_numero


titulo_tool("Calculadora de Aproveitamento de Papel")

with st.form("form_calculadora"):
    linha1_col1, linha1_col2 = st.columns(2)

    with linha1_col1:
        papel_largura_txt = st.text_input("Largura do papel (mm)", placeholder="Digite...")

    with linha1_col2:
        papel_altura_txt = st.text_input("Altura do papel (mm)", placeholder="Digite...")

    linha2_col1, linha2_col2 = st.columns(2)

    with linha2_col1:
        peca_largura_txt = st.text_input("Largura da peça (mm)", placeholder="Digite...")

    with linha2_col2:
        peca_altura_txt = st.text_input("Altura da peça (mm)", placeholder="Digite...")

    quantidade_pecas_txt = st.text_input(
        "Quantidade de peças (opcional)",
        placeholder="Digite se quiser calcular planos..."
    )

    papel_largura = converter_numero(papel_largura_txt)
    papel_altura = converter_numero(papel_altura_txt)
    peca_largura = converter_numero(peca_largura_txt)
    peca_altura = converter_numero(peca_altura_txt)
    quantidade_pecas = converter_numero(quantidade_pecas_txt)

    linha_final_1, linha_final_2, linha_final_3, linha_final_4 = st.columns([1.05, 1.05, 1.7, 0.7])

    with linha_final_1:
        espaco = st.number_input("Espaço", value=5, min_value=0, key="espaco")

    with linha_final_2:
        margem = st.number_input("Margem", value=5, min_value=0, key="margem")

    with linha_final_3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        melhor = st.form_submit_button("Melhor Montagem", type="primary", use_container_width=True)

    with linha_final_4:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        segunda = st.form_submit_button("2ª opção", use_container_width=True)


def calcular(papel_l, papel_a, peca_l, peca_a, espaco, margem, quantidade=None):
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

    area_folha = papel_l * papel_a
    area_pecas = total * peca_l * peca_a
    aproveitamento = (area_pecas / area_folha) * 100 if area_folha > 0 else 0
    desperdicio = 100 - aproveitamento

    planos = None
    pecas_produzidas = None

    if quantidade is not None and quantidade > 0 and total > 0:
        planos = math.ceil(quantidade / total)
        pecas_produzidas = total * planos

    return {
        "peca_l": peca_l,
        "peca_a": peca_a,
        "colunas": colunas,
        "linhas": linhas,
        "total": total,
        "inicio_x": inicio_x,
        "inicio_y": inicio_y,
        "largura_ocupada": largura_ocupada,
        "altura_ocupada": altura_ocupada,
        "aproveitamento": aproveitamento,
        "desperdicio": desperdicio,
        "sobra_lateral": area_util_l - largura_ocupada,
        "sobra_superior": area_util_a - altura_ocupada,
        "planos": planos,
        "pecas_produzidas": pecas_produzidas,
    }


def obter_opcoes():
    normal = calcular(papel_largura, papel_altura, peca_largura, peca_altura, espaco, margem, quantidade_pecas)
    normal["orientacao"] = "Peça normal"

    rotacionado = calcular(papel_largura, papel_altura, peca_altura, peca_largura, espaco, margem, quantidade_pecas)
    rotacionado["orientacao"] = "Peça rotacionada 90°"

    return sorted([normal, rotacionado], key=lambda opcao: opcao["total"], reverse=True)


def mostrar_cards(resultado):
    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

    if resultado["planos"] is None:
        c1, c2 = st.columns(2)
        with c1:
            card("Peças por plano", resultado["total"], f'{resultado["colunas"]} × {resultado["linhas"]}')
        with c2:
            card("Aproveitamento", f'{resultado["aproveitamento"]:.1f}%', "área ocupada")
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            card("Peças por plano", resultado["total"], f'{resultado["colunas"]} × {resultado["linhas"]}')
        with c2:
            card("Aproveitamento", f'{resultado["aproveitamento"]:.1f}%', "área ocupada")
        with c3:
            card("Planos a imprimir", resultado["planos"], f"para {int(quantidade_pecas)} peças")
        with c4:
            excedente = int(resultado["pecas_produzidas"] - quantidade_pecas)
            card("Produção final", resultado["pecas_produzidas"], f"+{excedente} excedente")

    st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)


def desenhar(resultado):
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.add_patch(patches.Rectangle((0, 0), papel_largura, papel_altura, fill=False, linewidth=2, edgecolor="black"))

    ax.add_patch(
        patches.Rectangle(
            (margem, margem),
            papel_largura - margem * 2,
            papel_altura - margem * 2,
            fill=False,
            linestyle="--",
            linewidth=0.7,
            edgecolor="0.65",
        )
    )

    for linha in range(resultado["linhas"]):
        for coluna in range(resultado["colunas"]):
            x = resultado["inicio_x"] + coluna * (resultado["peca_l"] + espaco)
            y = resultado["inicio_y"] + linha * (resultado["peca_a"] + espaco)
            ax.add_patch(patches.Rectangle((x, y), resultado["peca_l"], resultado["peca_a"], fill=False, linewidth=1, edgecolor="black"))

    ax.set_xlim(0, papel_largura)
    ax.set_ylim(0, papel_altura)
    ax.set_aspect("equal")
    ax.set_title(
        f'{resultado["orientacao"]} | {resultado["colunas"]} x {resultado["linhas"]} = {resultado["total"]} peças',
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig


campos_principais_ok = all([
    papel_largura is not None and papel_largura > 0,
    papel_altura is not None and papel_altura > 0,
    peca_largura is not None and peca_largura > 0,
    peca_altura is not None and peca_altura > 0,
])

if melhor or segunda:
    if not campos_principais_ok:
        st.warning("Preencha papel e peça antes de calcular. A quantidade pode ficar vazia.")
    else:
        opcoes = obter_opcoes()
        resultado = opcoes[0] if melhor else opcoes[1]

        mostrar_cards(resultado)
        st.pyplot(desenhar(resultado))

        if melhor:
            st.success(f"Melhor opção: {resultado['orientacao']}")
        else:
            st.warning(f"Opção exibida: {resultado['orientacao']}")

        if quantidade_pecas is not None and quantidade_pecas > 0:
            st.write(f"Quantidade total: **{int(quantidade_pecas)} peças**")
            st.write(f"Planos a imprimir: **{resultado['planos']}**")

        st.write(f"Montagem: **{resultado['colunas']} colunas × {resultado['linhas']} linhas**")
        st.write(f"Tamanho usado da peça: **{resultado['peca_l']} × {resultado['peca_a']} mm**")
        st.write(f"Espaço entre peças: **{espaco} mm**")
        st.write(f"Margem de segurança: **{margem} mm**")
