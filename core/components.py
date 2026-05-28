"""Componentes visuais reutilizáveis."""
import streamlit as st


def aplicar_estilo_global():
    from .styles import carregar_css
    st.markdown(carregar_css(), unsafe_allow_html=True)


def marca_topo():
    st.markdown('<div class="m87-brand">BY @M87 • TOOLS</div>', unsafe_allow_html=True)


def titulo_tool(titulo, descricao=None):
    marca_topo()
    st.subheader(titulo)
    if descricao:
        st.caption(descricao)


def card(label, value, extra=""):
    st.markdown(
        f"""
        <div class="card-m87">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-extra">{extra}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
