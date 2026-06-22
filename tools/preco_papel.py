import streamlit as st

from core.components import card, titulo_tool
from core.utils import converter_numero


titulo_tool("Calculadora de Valor de Papel")

with st.form("form_valor_papel"):

    linha1_col1, linha1_col2, linha1_col3 = st.columns([1, 1, 0.7])

    with linha1_col1:
        papel_largura_txt = st.text_input("Largura do papel (mm)")

    with linha1_col2:
        papel_altura_txt = st.text_input("Altura do papel (mm)")

    with linha1_col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        inverter_papel = st.checkbox("Inverter medidas", key="inverter_papel_valor")

    linha2_col1, linha2_col2, linha2_col3 = st.columns([1, 1, 0.7])

    with linha2_col1:
        gramatura_txt = st.text_input("Gramatura (g/m²)")

    with linha2_col2:
        preco_kg_txt = st.text_input("Preço do quilo (€)")

    with linha2_col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        quantidade_folhas_txt = st.text_input("Folhas (opcional)")

    linha_final_1, linha_final_2 = st.columns([1.7, 0.7])

    with linha_final_1:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        calcular_btn = st.form_submit_button("Calcular valor", type="primary", use_container_width=True)

    with linha_final_2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        limpar_btn = st.form_submit_button("Limpar", use_container_width=True)

    papel_largura = converter_numero(papel_largura_txt)
    papel_altura = converter_numero(papel_altura_txt)
    gramatura = converter_numero(gramatura_txt)
    preco_kg = converter_numero(preco_kg_txt)
    quantidade_folhas = converter_numero(quantidade_folhas_txt)

    if papel_largura is not None and papel_altura is not None and inverter_papel:
        papel_largura, papel_altura = papel_altura, papel_largura


def formatar_euro(valor):
    return f"€ {valor:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_valor_papel(largura_mm, altura_mm, gramatura_gm2, preco_por_kg, quantidade=None):
    area_m2 = (largura_mm / 1000) * (altura_mm / 1000)
    peso_folha_kg = (area_m2 * gramatura_gm2) / 1000

    folhas_por_kg = 1 / peso_folha_kg
    preco_folha = preco_por_kg * peso_folha_kg
    preco_500_folhas = preco_folha * 500

    peso_total_kg = None
    custo_total = None

    if quantidade is not None and quantidade > 0:
        peso_total_kg = peso_folha_kg * quantidade
        custo_total = preco_folha * quantidade

    return {
        "area_m2": area_m2,
        "peso_folha_kg": peso_folha_kg,
        "peso_folha_g": peso_folha_kg * 1000,
        "folhas_por_kg": folhas_por_kg,
        "preco_folha": preco_folha,
        "preco_500_folhas": preco_500_folhas,
        "peso_total_kg": peso_total_kg,
        "custo_total": custo_total,
    }


def mostrar_cards(resultado):
    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

    if resultado["custo_total"] is None:
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card("Folhas por kg", formatar_numero(resultado["folhas_por_kg"], 1), "aprox.")

        with c2:
            card("Preço por folha", formatar_euro(resultado["preco_folha"]), "valor unitário")

        with c3:
            card("Peso por folha", f'{formatar_numero(resultado["peso_folha_g"], 2)} g', "1 folha")

        with c4:
            card("500 folhas", formatar_euro(resultado["preco_500_folhas"]), "referência")

    else:
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card("Folhas por kg", formatar_numero(resultado["folhas_por_kg"], 1), "aprox.")

        with c2:
            card("Preço por folha", formatar_euro(resultado["preco_folha"]), "valor unitário")

        with c3:
            card("Peso total", f'{formatar_numero(resultado["peso_total_kg"], 3)} kg', "quantidade")

        with c4:
            card("Custo total", formatar_euro(resultado["custo_total"]), "papel")

    st.markdown("<div style='height:45px'></div>", unsafe_allow_html=True)


campos_ok = all([
    papel_largura is not None and papel_largura > 0,
    papel_altura is not None and papel_altura > 0,
    gramatura is not None and gramatura > 0,
    preco_kg is not None and preco_kg > 0,
])

if calcular_btn:
    if not campos_ok:
        st.warning("Preencha largura, altura, gramatura e preço do quilo antes de calcular.")
    else:
        resultado = calcular_valor_papel(
            papel_largura,
            papel_altura,
            gramatura,
            preco_kg,
            quantidade_folhas,
        )

        mostrar_cards(resultado)

        st.success("Cálculo concluído")

        st.write(f"Formato do papel: **{papel_largura} × {papel_altura} mm**")
        st.write(f"Área da folha: **{formatar_numero(resultado['area_m2'], 4)} m²**")
        st.write(f"Gramatura: **{gramatura} g/m²**")
        st.write(f"Preço do quilo: **{formatar_euro(preco_kg)}**")

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

        st.write("Conta usada:")

        st.code(
            "peso da folha em kg = largura(m) × altura(m) × gramatura(g/m²) / 1000\n"
            "folhas por kg = 1 / peso da folha em kg\n"
            "preço por folha = preço do kg × peso da folha em kg",
            language="text",
        )

        if quantidade_folhas is not None and quantidade_folhas > 0:
            st.write(f"Quantidade calculada: **{int(quantidade_folhas)} folhas**")
            st.write(f"Peso total: **{formatar_numero(resultado['peso_total_kg'], 3)} kg**")
            st.write(f"Custo total: **{formatar_euro(resultado['custo_total'])}**")

if limpar_btn:
    st.info("Para limpar os campos, apague os valores e calcule novamente.")