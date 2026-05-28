import pandas as pd
import streamlit as st

from core.components import titulo_tool
from core.rules import STANDARD_FORMATS


titulo_tool(
    "Biblioteca de Formatos Padrão",
    "Consulta rápida de medidas usadas em gráfica e pré-impressão."
)

df = pd.DataFrame(STANDARD_FORMATS)
df = df.rename(columns={"nome": "Formato", "largura": "Largura (mm)", "altura": "Altura (mm)", "categoria": "Categoria"})

categoria = st.selectbox("Categoria", ["Todos"] + sorted(df["Categoria"].unique().tolist()))

if categoria != "Todos":
    df_filtrado = df[df["Categoria"] == categoria]
else:
    df_filtrado = df

busca = st.text_input("Buscar formato", placeholder="Ex: A4, SRA3, cartão...")

if busca:
    termo = busca.lower()
    df_filtrado = df_filtrado[df_filtrado.apply(lambda linha: termo in " ".join(linha.astype(str)).lower(), axis=1)]

st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
