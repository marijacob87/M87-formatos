import streamlit as st

from core.components import aplicar_estilo_global

st.set_page_config(
    page_title="M87 Tools",
    layout="centered",
    initial_sidebar_state="expanded"
)

aplicar_estilo_global()

paginas = [
    st.Page("tools/calculadora_formatos.py", title="Calculadora de Formatos", default=True),
    st.Page("tools/peso_papel.py", title="Calculadora Peso de Papel"),
    st.Page("tools/area_m2.py", title="Calculadora de Área m²"),
    st.Page("tools/checklist_pre_impressao.py", title="Checklist Pré-Impressão"),
    st.Page("tools/biblioteca_formatos.py", title="Biblioteca de Formatos"),
]

navegacao = st.navigation(paginas, position="sidebar")
navegacao.run()
