import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


st.set_page_config(
    page_title="M87 • Calculadora de Formatos",
    layout="centered"
)
st.markdown(
    """
    <div style="
        text-align: center;
        color: #C98A1A;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0px;
        margin-bottom: 12px;
    ">
        BY @M87 • TOOLS
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        .card-m87 {
            background: linear-gradient(135deg, #111827, #1f2937);
            border: 1px solid #374151;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 10px 24px rgba(0,0,0,0.18);
            min-height: 65px;
            margin-bottom: 0px;
        }

        .card-label {
            font-size: 9px;
            color: #9CA3AF;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .card-value {
            font-size: 30px;
            color: #FFFFFF;
            font-weight: 800;
            line-height: 1;
        }

        .card-extra {
            font-size: 12px;
            color: #D1D5DB;
            margin-top: 7px;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #C98A1A !important;
            border: 1px solid #C98A1A !important;
            color: white !important;
            font-weight: 800;
            border-radius: 10px;
            height: 58px;
            font-size: 18px;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background-color: #D99A27 !important;
            border: 1px solid #D99A27 !important;
        }

        div[data-testid="stButton"] > button[kind="secondary"] {
            height: 58px !important;
            font-size: 5px !important;
            padding: 4px 18px !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("Calculadora de Aproveitamento de Papel")


# ==================================================
# PAINEL VISUAL
# ==================================================

linha1_col1, linha1_col2 = st.columns(2)

with linha1_col1:
    papel_largura = st.number_input(
        "Largura do papel (mm)",
        value=none,
        min_value=1,
        key="papel_largura"
    )

with linha1_col2:
    papel_altura = st.number_input(
        "Altura do papel (mm)",
        value=none,
        min_value=1,
        key="papel_altura"
    )


linha2_col1, linha2_col2 = st.columns(2)

with linha2_col1:
    peca_largura = st.number_input(
        "Largura da peça (mm)",
        value=none,
        min_value=1,
        key="peca_largura"
    )

with linha2_col2:
    peca_altura = st.number_input(
        "Altura da peça (mm)",
        value=none,
        min_value=1,
        key="peca_altura"
    )


quantidade_pecas = st.number_input(
    "Quantidade de peças",
    value=none,
    min_value=1,
    key="quantidade_pecas"
)


# ==================================================
# CONFIGURAÇÕES + BOTÕES
# ==================================================

linha_final_1, linha_final_2, linha_final_3, linha_final_4 = st.columns([1.05, 1.05, 1.7, 0.7])

with linha_final_1:
    espaco = st.number_input(
        "Espaço",
        value=5,
        min_value=0,
        key="espaco"
    )

with linha_final_2:
    margem = st.number_input(
        "Margem",
        value=5,
        min_value=0,
        key="margem"
    )

with linha_final_3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    melhor = st.button(
        "Melhor Montagem",
        type="primary",
        use_container_width=True
    )

with linha_final_4:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    segunda = st.button(
    "2ª opção",
    use_container_width=True
)


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

    area_folha = papel_l * papel_a
    area_pecas = total * peca_l * peca_a

    aproveitamento = (area_pecas / area_folha) * 100 if area_folha > 0 else 0
    desperdicio = 100 - aproveitamento

    sobra_lateral = area_util_l - largura_ocupada
    sobra_superior = area_util_a - altura_ocupada

    planos = math.ceil(quantidade_pecas / total) if total > 0 else 0

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
        "sobra_lateral": sobra_lateral,
        "sobra_superior": sobra_superior,
        "planos": planos
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
# CARDS
# ==================================================

def mostrar_cards(resultado):
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="card-m87">
                <div class="card-label">Peças por plano</div>
                <div class="card-value">{resultado["total"]}</div>
                <div class="card-extra">{resultado["colunas"]} × {resultado["linhas"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="card-m87">
                <div class="card-label">Aproveitamento</div>
                <div class="card-value">{resultado["aproveitamento"]:.1f}%</div>
                <div class="card-extra">área ocupada</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="card-m87">
                <div class="card-label">Planos a imprimir</div>
                <div class="card-value">{resultado["planos"]}</div>
                <div class="card-extra">para {quantidade_pecas} peças</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            """
            <div class="card-m87">
                <div class="card-label">&nbsp;</div>
                <div class="card-value">&nbsp;</div>
                <div class="card-extra">&nbsp;</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:45px'></div>", unsafe_allow_html=True)


# ==================================================
# DESENHO
# ==================================================

def desenhar(resultado):
    fig, ax = plt.subplots(figsize=(9, 6))

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
# RESULTADO
# ==================================================

opcoes = obter_opcoes()

if melhor:
    resultado = opcoes[0]

    mostrar_cards(resultado)
    st.pyplot(desenhar(resultado))

    st.success(f"Melhor opção: {resultado['orientacao']}")
    st.write(f"Quantidade total: **{quantidade_pecas} peças**")
    st.write(f"Planos a imprimir: **{resultado['planos']}**")
    st.write(f"Montagem: **{resultado['colunas']} colunas × {resultado['linhas']} linhas**")
    st.write(f"Tamanho usado da peça: **{resultado['peca_l']} × {resultado['peca_a']} mm**")
    st.write(f"Espaço entre peças: **{espaco} mm**")
    st.write(f"Margem de segurança: **{margem} mm**")


if segunda:
    resultado = opcoes[1]

    mostrar_cards(resultado)
    st.pyplot(desenhar(resultado))

    st.warning(f"Opção exibida: {resultado['orientacao']}")
    st.write(f"Quantidade total: **{quantidade_pecas} peças**")
    st.write(f"Planos a imprimir: **{resultado['planos']}**")
    st.write(f"Montagem: **{resultado['colunas']} colunas × {resultado['linhas']} linhas**")
    st.write(f"Tamanho usado da peça: **{resultado['peca_l']} × {resultado['peca_a']} mm**")
    st.write(f"Espaço entre peças: **{espaco} mm**")
    st.write(f"Margem de segurança: **{margem} mm**")
