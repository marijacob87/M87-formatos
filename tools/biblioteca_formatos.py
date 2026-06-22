import pandas as pd
import streamlit as st

from core.components import titulo_tool
from core.rules import STANDARD_FORMATS


titulo_tool("Formatos")


st.markdown(
    """
    <style>
        .formato-row {
            padding: 0 !important;
            margin: 0 !important;
            line-height: 0.9 !important;
        }

        .formato-nome {
            font-weight: 700;
            font-size: 0.92rem;
            margin: 0 !important;
            padding: 0 !important;
        }

        .formato-medida {
            font-size: 0.92rem;
            margin: 0 !important;
            padding: 0 !important;
            color: rgba(255,255,255,0.82);
        }

        .formato-separador {
            height: 1px;
            background: rgba(255,255,255,0.04);
            margin: 0 !important;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 0.3rem !important;
        }

        [data-testid="column"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def normalizar_busca(texto):
    if texto is None:
        return ""

    texto = str(texto).lower().strip()
    texto = texto.replace(",", ".")
    texto = texto.replace("×", "x")
    texto = texto.replace(" mm", "")
    texto = texto.replace("mm", "")
    texto = texto.replace(" ", "")

    return texto


def formatar_numero(valor):
    valor = round(valor, 2)

    if valor == int(valor):
        return str(int(valor))

    return str(valor).replace(".", ",")


def montar_dataframe_formatos():
    df = pd.DataFrame(STANDARD_FORMATS)

    df = df.rename(
        columns={
            "nome": "Formato",
            "largura": "Largura (mm)",
            "altura": "Altura (mm)",
        }
    )

    df = df[["Formato", "Largura (mm)", "Altura (mm)"]]

    df["Medida"] = (
        df["Largura (mm)"].astype(str)
        + " x "
        + df["Altura (mm)"].astype(str)
        + " mm"
    )

    return df


def usar_formato(largura, altura):
    st.session_state["formato_largura_original"] = float(largura)
    st.session_state["formato_altura_original"] = float(altura)
    st.session_state["formatos_aba_atual"] = "Proporção"


if "formato_largura_original" not in st.session_state:
    st.session_state["formato_largura_original"] = 0.0

if "formato_altura_original" not in st.session_state:
    st.session_state["formato_altura_original"] = 0.0

if "formatos_aba_atual" not in st.session_state:
    st.session_state["formatos_aba_atual"] = "Proporção"


aba_atual = st.segmented_control(
    "Área da ferramenta",
    ["Proporção", "Biblioteca"],
    default=st.session_state["formatos_aba_atual"],
    key="formatos_aba_atual",
    label_visibility="collapsed"
)


if aba_atual == "Proporção":
    st.markdown("### Redimensionar proporcionalmente")

    st.caption(
        """
        Redimensione uma arte sem distorcer. (Consulte formatos padrão na Biblioteca.)

        • Informe a medida original

        • Escolha calcular por nova medida ou escala

        • Digite a medida desejada
        """
    )

    col_largura, col_altura = st.columns(2)

    with col_largura:
        largura_original = st.number_input(
            "Largura original (mm)",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            key="formato_largura_original"
        )

    with col_altura:
        altura_original = st.number_input(
            "Altura original (mm)",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            key="formato_altura_original"
        )

    modo = st.segmented_control(
        "Calcular por",
        ["Nova medida", "Escala %"],
        default="Nova medida",
        key="formato_modo_calculo"
    )

    if modo == "Nova medida":
        base_calculo = st.segmented_control(
            "Redimensionar pela",
            ["Largura", "Altura"],
            default="Largura",
            key="formato_base_calculo"
        )

        nova_medida = st.number_input(
            f"Nova {base_calculo.lower()} desejada (mm)",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            key="formato_nova_medida"
        )

    else:
        escala_percentual = st.number_input(
            "Escala desejada (%)",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            key="formato_escala_percentual"
        )

    if largura_original > 0 and altura_original > 0:
        nova_largura = None
        nova_altura = None
        escala = None

        if modo == "Nova medida" and nova_medida > 0:
            if base_calculo == "Largura":
                escala = nova_medida / largura_original
                nova_largura = nova_medida
                nova_altura = altura_original * escala
            else:
                escala = nova_medida / altura_original
                nova_altura = nova_medida
                nova_largura = largura_original * escala

        elif modo == "Escala %" and escala_percentual > 0:
            escala = escala_percentual / 100
            nova_largura = largura_original * escala
            nova_altura = altura_original * escala

        if nova_largura and nova_altura and escala:
            st.markdown("### Resultado")

            col_resultado, col_escala = st.columns(2)

            with col_resultado:
                st.metric(
                    "Nova medida",
                    f"{formatar_numero(nova_largura)} x {formatar_numero(nova_altura)} mm"
                )

            with col_escala:
                st.metric(
                    "Escala",
                    f"{formatar_numero(escala * 100)}%"
                )


else:
    st.markdown("### Biblioteca de formatos")

    st.caption(
        "Use a Biblioteca para consultar medidas padrão. "
        "Ao clicar em “Usar”, a largura e a altura do formato escolhido são enviadas "
        "para Proporção como medida original."
    )

    df = montar_dataframe_formatos()

    busca = st.text_input(
        "Buscar por formato ou medida",
        placeholder="Ex: A4, SRA3, 210x297, 85 x 55..."
    )

    df_filtrado = df.copy()

    if busca:
        termo = normalizar_busca(busca)

        df_filtrado = df_filtrado[
            df_filtrado.apply(
                lambda linha: (
                    termo in normalizar_busca(linha["Formato"])
                    or termo in normalizar_busca(linha["Medida"])
                    or termo in normalizar_busca(
                        f'{linha["Largura (mm)"]}x{linha["Altura (mm)"]}'
                    )
                    or termo in normalizar_busca(
                        f'{linha["Altura (mm)"]}x{linha["Largura (mm)"]}'
                    )
                ),
                axis=1,
            )
        ]

    if df_filtrado.empty:
        st.warning("Nenhum formato encontrado.")
    else:
        for indice, linha in df_filtrado.iterrows():
            col_nome, col_medida, col_botao = st.columns([2.4, 1.4, 0.55])

            with col_nome:
                st.markdown(
                    f"<div class='formato-row formato-nome'>{linha['Formato']}</div>",
                    unsafe_allow_html=True
                )

            with col_medida:
                st.markdown(
                    f"<div class='formato-row formato-medida'>{linha['Medida']}</div>",
                    unsafe_allow_html=True
                )

            with col_botao:
                st.button(
                    "Usar",
                    key=f"usar_formato_{indice}",
                    on_click=usar_formato,
                    args=(linha["Largura (mm)"], linha["Altura (mm)"])
                )

            st.markdown(
                "<div class='formato-separador'></div>",
                unsafe_allow_html=True
            )