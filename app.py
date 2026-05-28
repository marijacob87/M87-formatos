import streamlit as st

st.set_page_config(
    page_title="M87 • Tools",
    layout="centered"
)

st.markdown(
    """
    <div style="
        text-align: center;
        color: #C98A1A;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0px;
        margin-bottom: 12px;
    ">
        BY @M87 • TOOLS
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        .hero-m87 {
            background: linear-gradient(135deg, #111827, #1f2937);
            border: 1px solid #374151;
            border-radius: 16px;
            padding: 26px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.18);
            margin-bottom: 22px;
        }
        .hero-title {
            color: #FFFFFF;
            font-size: 34px;
            font-weight: 900;
            margin-bottom: 8px;
        }
        .hero-text {
            color: #D1D5DB;
            font-size: 15px;
            line-height: 1.5;
        }
        .tool-card {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
        }
        .tool-title {
            font-weight: 800;
            font-size: 17px;
            color: #111827;
        }
        .tool-text {
            color: #4B5563;
            font-size: 13px;
            margin-top: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-m87">
        <div class="hero-title">M87 Tools</div>
        <div class="hero-text">
            Mini central de ferramentas para gráfica, pré-impressão e produção.
            Escolha uma aplicação no menu lateral esquerdo.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("## M87 Tools")
st.sidebar.markdown("Aplicações rápidas para gráfica e pré-impressão.")

st.subheader("Aplicações disponíveis")

cards = [
    ("Calculadora de formatos", "Aproveitamento de papel, montagem, quantidade por plano e folhas necessárias."),
    ("Calculadora de peso de papel", "Calcula peso total em kg usando formato, gramatura e quantidade."),
    ("Calculadora de área em m²", "Converte largura × altura × quantidade em metros quadrados."),
    ("Checklist pré-impressão", "Lista rápida para conferir arquivos antes de enviar para produção."),
    ("Biblioteca de formatos padrão", "Consulta rápida de medidas A, B, SRA e formatos gráficos comuns."),
]

for titulo, texto in cards:
    st.markdown(
        f"""
        <div class="tool-card">
            <div class="tool-title">{titulo}</div>
            <div class="tool-text">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.info("Use o menu lateral para abrir cada ferramenta.")
