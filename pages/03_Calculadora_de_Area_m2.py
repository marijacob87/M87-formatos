import streamlit as st

st.set_page_config(page_title="M87 • Área em m²", layout="centered")

st.markdown("""
<div style="text-align:center;color:#C98A1A;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
BY @M87 • TOOLS
</div>
""", unsafe_allow_html=True)

st.subheader("Calculadora de Área em m²")
st.caption("Para papel, adesivo, lona, vinil, placa, banner e materiais vendidos por área.")


def converter_numero(valor):
    if valor == "":
        return None
    try:
        return float(valor.replace(",", "."))
    except ValueError:
        return None

with st.form("form_area"):
    unidade = st.selectbox("Unidade informada", ["mm", "cm", "m"])

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
        if unidade == "mm":
            largura_m = largura / 1000
            altura_m = altura / 1000
        elif unidade == "cm":
            largura_m = largura / 100
            altura_m = altura / 100
        else:
            largura_m = largura
            altura_m = altura

        area_unitaria = largura_m * altura_m
        area_total = area_unitaria * quantidade

        st.success("Área calculada")
        c1, c2 = st.columns(2)
        c1.metric("Área unitária", f"{area_unitaria:.3f} m²")
        c2.metric("Área total", f"{area_total:.3f} m²")
