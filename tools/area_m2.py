import streamlit as st

from core.components import card, titulo_tool
from core.rules import AREA_UNITS
from core.utils import converter_numero


titulo_tool(
    "Calculadora de Área em m²",
    "Para papel, adesivo, lona, vinil, placa, banner e materiais vendidos por área."
)

with st.form("form_area"):
    unidade = st.selectbox("Unidade informada", list(AREA_UNITS.keys()))

    col1, col2 = st.columns(2)
    with col1:
        largura_txt = st.text_input("Largura", placeholder="Ex: 700")
    with col2:
        altura_txt = st.text_input("Altura", placeholder="Ex: 1000")

    quantidade_txt = st.text_input("Quantidade", placeholder="Ex: 1", value="1")
    calcular = st.form_submit_button("Calcular área", type="primary", use_container_width=True)

largura = converter_numero(largura_txt)
altura = converter_numero(altura_txt)
quantidade = converter_numero(quantidade_txt)

if calcular:
    campos_ok = all([
        largura is not None and largura > 0,
        altura is not None and altura > 0,
        quantidade is not None and quantidade > 0,
    ])

    if not campos_ok:
        st.warning("Preencha largura, altura e quantidade.")
    else:
        divisor = AREA_UNITS[unidade]
        largura_m = largura / divisor
        altura_m = altura / divisor
        area_unitaria = largura_m * altura_m
        area_total = area_unitaria * quantidade

        st.success("Área calculada")

        c1, c2 = st.columns(2)
        with c1:
            card("Área unitária", f"{area_unitaria:.3f} m²")
        with c2:
            card("Área total", f"{area_total:.3f} m²", f"{int(quantidade)} un.")
