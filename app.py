import streamlit as st

st.set_page_config(
    page_title="M87 Tools",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        section[data-testid="stSidebar"] {
            min-width: 310px !important;
            width: 310px !important;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 26px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

paginas = [
    st.Page(
        "tools/formatos.py",
        title="Calculadora de Formatos",
        icon="📐",
        default=True
    ),
    st.Page(
        "tools/peso_papel.py",
        title="Calculadora de Peso de Papel",
        icon="⚖️"
    ),
    st.Page(
        "tools/area_m2.py",
        title="Calculadora de Área m²",
        icon="◻️"
    ),
    st.Page(
        "tools/checklist_pre_impressao.py",
        title="Checklist Pré-Impressão",
        icon="✅"
    ),
    st.Page(
        "tools/biblioteca_formatos.py",
        title="Biblioteca de Formatos Padrão",
        icon="📚"
    ),
]

navegacao = st.navigation(paginas, position="sidebar")
navegacao.run()
