import streamlit as st

from core.components import titulo_tool
from core.rules import PREPRESS_CHECKLIST


titulo_tool(
    "Checklist Pré-Impressão",
    "Uma lista rápida para não mandar um PDF possuído para produção."
)

marcados = []

for item in PREPRESS_CHECKLIST:
    if st.checkbox(item):
        marcados.append(item)

total = len(PREPRESS_CHECKLIST)
feito = len(marcados)
percentual = feito / total if total else 0

st.progress(percentual)
st.write(f"Conferido: **{feito}/{total}**")

if feito == total:
    st.success("Arquivo pronto para produção.")
elif feito >= total * 0.75:
    st.info("Quase lá. Ainda tem alguns fantasminhas no PDF.")
else:
    st.warning("Ainda faltam pontos importantes antes de enviar.")
