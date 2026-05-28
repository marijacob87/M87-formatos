import streamlit as st


st.markdown("""
<div style="text-align:center;color:#C98A1A;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
BY @M87 • TOOLS
</div>
""", unsafe_allow_html=True)

st.subheader("Calculadora de Peso de Papel")
st.caption("Calcula o peso total a partir do formato, gramatura e quantidade.")


def converter_numero(valor):
    if valor == "":
        return None
    try:
        return float(valor.replace(",", "."))
    except ValueError:
        return None

with st.form("form_peso"):
    col1, col2 = st.columns(2)

    with col1:
        largura_txt = st.text_input("Largura da folha/peça (mm)", placeholder="Ex: 700")
        gramatura_txt = st.text_input("Gramatura (g/m²)", placeholder="Ex: 100")

    with col2:
        altura_txt = st.text_input("Altura da folha/peça (mm)", placeholder="Ex: 1000")
        quantidade_txt = st.text_input("Quantidade", placeholder="Ex: 500")

    calcular = st.form_submit_button("Calcular peso", type="primary", use_container_width=True)

largura = converter_numero(largura_txt)
altura = converter_numero(altura_txt)
gramatura = converter_numero(gramatura_txt)
quantidade = converter_numero(quantidade_txt)

if calcular:
    campos_ok = all([
        largura is not None and largura > 0,
        altura is not None and altura > 0,
        gramatura is not None and gramatura > 0,
        quantidade is not None and quantidade > 0,
    ])

    if not campos_ok:
        st.warning("Preencha largura, altura, gramatura e quantidade.")
    else:
        area_m2 = (largura / 1000) * (altura / 1000)
        peso_kg = area_m2 * gramatura * quantidade / 1000

        st.success("Peso calculado")
        c1, c2, c3 = st.columns(3)
        c1.metric("Área unitária", f"{area_m2:.3f} m²")
        c2.metric("Peso total", f"{peso_kg:.2f} kg")
        c3.metric("Quantidade", f"{int(quantidade)}")

        st.write(f"Conta: **{largura:g} × {altura:g} mm**, **{gramatura:g} g/m²**, **{int(quantidade)} folhas/peças**.")
