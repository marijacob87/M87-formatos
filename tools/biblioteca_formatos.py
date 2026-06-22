import pandas as pd
import streamlit as st

from core.components import titulo_tool
from core.rules import STANDARD_FORMATS


titulo_tool(
    "Formatos",
    "Redimensione uma arte sem distorcer: informe a medida original, escolha se quer calcular por nova medida ou escala, e consulte formatos padrão na Biblioteca."
)


def normalizar_busca(texto):
    """Padroniza a busca para aceitar nome, medida com x, ×, vírgula ou espaços."""
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
    """Mostra números com vírgula e sem zeros desnecessários."""
    valor = round(valor, 2)

    if valor == int(valor):
        return str(int(valor))

    return str(valor).replace(".", ",")


aba_proporcao, aba_biblioteca = st.tabs(
    ["Proporção", "Biblioteca"]
)


with aba_proporcao:
    st.markdown("### Redimensionar proporcionalmente")

    col_largura, col_altura = st.columns(2)

    with col_largura:
        largura_original = st.number_input(
            "Largura original (mm)",
            min_value=0.0,
            step=0.1,
            format="%.2f"
        )

    with col_altura:
        altura_original = st.number_input(
            "Altura original (mm)",
            min_value=0.0,
            step=0.1,
            format="%.2f"
        )

    modo = st.segmented_control(
        "Calcular por",
        ["Nova medida", "Escala %"],
        default="Nova medida"
    )

    if modo == "Nova medida":
        base_calculo = st.segmented_control(
            "Redimensionar pela",
            ["Largura", "Altura"],
            default="Largura"
        )

        nova_medida = st.number_input(
            f"Nova {base_calculo.lower()} desejada (mm)",
            min_value=0.0,
            step=0.1,
            format="%.2f"
        )

    else:
        escala_percentual = st.number_input(
            "Escala desejada (%)",
            min_value=0.0,
            step=0.1,
            format="%.2f"
        )

    if largura_original > 0 and altura_original > 0:
        if modo == "Nova medida":
            if nova_medida > 0:
                if base_calculo == "Largura":
                    escala = nova_medida / largura_original
                    nova_largura = nova_medida
                    nova_altura = altura_original * escala
                else:
                    escala = nova_medida / altura_original
                    nova_altura = nova_medida
                    nova_largura = largura_original * escala

                st.success(
                    f"Resultado: {formatar_numero(nova_largura)} x "
                    f"{formatar_numero(nova_altura)} mm"
                )

                st.info(
                    f"Escala: {formatar_numero(escala * 100)}%"
                )

        else:
            if escala_percentual > 0:
                escala = escala_percentual / 100
                nova_largura = largura_original * escala
                nova_altura = altura_original * escala

                st.success(
                    f"Resultado: {formatar_numero(nova_largura)} x "
                    f"{formatar_numero(nova_altura)} mm"
                )

                st.info(
                    f"Escala: {formatar_numero(escala_percentual)}%"
                )


with aba_biblioteca:
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

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        height=720
    )