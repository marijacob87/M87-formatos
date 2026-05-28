import streamlit as st
import pandas as pd


st.markdown("""
<div style="text-align:center;color:#C98A1A;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
BY @M87 • TOOLS
</div>
""", unsafe_allow_html=True)

st.subheader("Biblioteca de Formatos Padrão")
st.caption("Consulta rápida de medidas usadas em gráfica e pré-impressão.")

formatos = [
    ("A0", 841, 1189, "ISO A"),
    ("A1", 594, 841, "ISO A"),
    ("A2", 420, 594, "ISO A"),
    ("A3", 297, 420, "ISO A"),
    ("A4", 210, 297, "ISO A"),
    ("A5", 148, 210, "ISO A"),
    ("A6", 105, 148, "ISO A"),
    ("SRA3", 320, 450, "SRA"),
    ("SRA4", 225, 320, "SRA"),
    ("Cartão de visita EU", 85, 55, "Comercial"),
    ("Cartão de visita alternativo", 90, 50, "Comercial"),
    ("Flyer DL", 99, 210, "Comercial"),
    ("Postal A6", 105, 148, "Comercial"),
]

df = pd.DataFrame(formatos, columns=["Formato", "Largura (mm)", "Altura (mm)", "Categoria"])

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
