import streamlit as st
import streamlit.components.v1 as components

from core.components import titulo_tool
from core.ean13 import (
    normalizar_ean13,
    gerar_ean13_svg,
    gerar_ean13_pdf,
    gerar_ean13_png,
    svg_para_base64,
)


titulo_tool("Código de Barras")


st.markdown(
    """
    <style>
        div[data-testid="stDownloadButton"] > button {
            height: 44px !important;
            border-radius: 12px !important;
            border: 1px solid #D99A16 !important;
            background: transparent !important;
            color: #D99A16 !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.2px !important;
        }

        div[data-testid="stDownloadButton"] > button p {
            color: #D99A16 !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            background: rgba(217, 154, 22, 0.10) !important;
            border-color: #E0A11A !important;
            color: #E0A11A !important;
        }

        div[data-testid="stDownloadButton"] > button:hover p {
            color: #E0A11A !important;
        }

        div[data-testid="stDownloadButton"] > button:disabled {
            border: 1px solid rgba(217, 154, 22, 0.45) !important;
            color: rgba(217, 154, 22, 0.45) !important;
            background: transparent !important;
            opacity: 1 !important;
        }

        div[data-testid="stDownloadButton"] > button:disabled p {
            color: rgba(217, 154, 22, 0.45) !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


tab_ean, tab_qr, tab_reader = st.tabs(
    ["EAN-13", "QR CODE", "LEITOR DE CÓDIGO"]
)


# =========================
# ABA 1 — EAN-13
# =========================

with tab_ean:
    codigo_ean = st.text_input(
        "Ao digitar 12 dígitos, o 13º será calculado automaticamente",
        max_chars=13,
        key="ean_codigo"
    ).strip()

    ean_final = None
    svg_ean = None
    pdf_ean = None
    png_ean = None

    ean_final, mensagem = normalizar_ean13(codigo_ean) if codigo_ean else (None, "")

    with st.expander("⚙ Opções avançadas"):
        col_dim1, col_dim2 = st.columns(2)

        with col_dim1:
            altura_barras = st.slider(
                "Altura visual das barras",
                min_value=10,
                max_value=80,
                value=26,
            )

        with col_dim2:
            escala = st.slider(
                "Escala",
                min_value=80,
                max_value=150,
                value=100,
            )

        mostrar_numeros = st.checkbox("Mostrar números", value=True)

        col_cor1, col_cor2 = st.columns(2)

        with col_cor1:
            cor_barras = st.color_picker("Cor das barras", "#000000")

        with col_cor2:
            fundo_transparente = st.checkbox("Fundo transparente", value=True)
            cor_fundo_picker = st.color_picker(
                "Cor de fundo",
                "#FFFFFF",
                disabled=fundo_transparente,
            )

        margem_adicional = st.number_input(
            "Zona de silêncio adicional (mm)",
            min_value=0.0,
            max_value=20.0,
            value=0.0,
            step=0.5,
        )

    if codigo_ean:
        if ean_final:
            cor_fundo = "transparent" if fundo_transparente else cor_fundo_picker

            largura_final = 37.29 * (escala / 100)
            altura_final = 25.93 * (escala / 100)

            svg_ean = gerar_ean13_svg(
                ean_final,
                largura_mm=largura_final,
                altura_mm=altura_final,
                cor_barras=cor_barras,
                cor_fundo=cor_fundo,
                mostrar_numeros=mostrar_numeros,
                margem_adicional_mm=margem_adicional,
                altura_barras_visual=altura_barras,
            )

            pdf_ean = gerar_ean13_pdf(
                ean_final,
                largura_mm=largura_final,
                altura_mm=altura_final,
                cor_barras=cor_barras,
                cor_fundo=cor_fundo,
                mostrar_numeros=mostrar_numeros,
                margem_adicional_mm=margem_adicional,
                altura_barras_visual=altura_barras,
            )

            png_ean = gerar_ean13_png(
                ean_final,
                largura_mm=largura_final,
                altura_mm=altura_final,
                cor_barras=cor_barras,
                cor_fundo=cor_fundo,
                mostrar_numeros=mostrar_numeros,
                margem_adicional_mm=margem_adicional,
                altura_barras_visual=altura_barras,
            )

        else:
            st.error(mensagem)

    st.markdown("#### Preview")

    col_preview, col_download = st.columns([3.85, 1.65], gap="large")

    with col_preview:
        if svg_ean:
            svg_base64 = svg_para_base64(svg_ean)

            components.html(
                f"""
                <div style="
                    background: transparent;
                    padding: 24px;
                    border: 1px solid rgba(255,255,255,.12);
                    border-radius: 12px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 360px;
                ">
                    <img
                        src="data:image/svg+xml;base64,{svg_base64}"
                        style="
                            background: white;
                            padding: 12px;
                            width: 660px;
                            max-width: 100%;
                            height: auto;
                        ">
                </div>
                """,
                height=430,
            )
        else:
            st.info("Digite um EAN-13 válido para ver o preview.")

    with col_download:
        st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)

        st.download_button(
            "⬇  Baixar SVG",
            data=svg_ean if svg_ean else b"",
            file_name=f"EAN13_{ean_final}.svg" if ean_final else "EAN13.svg",
            mime="image/svg+xml",
            use_container_width=True,
            type="secondary",
            disabled=not bool(svg_ean),
        )

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

        st.download_button(
            "⬇  Baixar PDF",
            data=pdf_ean if pdf_ean else b"",
            file_name=f"EAN13_{ean_final}.pdf" if ean_final else "EAN13.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="secondary",
            disabled=not bool(pdf_ean),
        )

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

        st.download_button(
            "⬇  Baixar PNG",
            data=png_ean if png_ean else b"",
            file_name=f"EAN13_{ean_final}.png" if ean_final else "EAN13.png",
            mime="image/png",
            use_container_width=True,
            type="secondary",
            disabled=not bool(png_ean),
        )


# =========================
# ABA 2 — QR CODE
# =========================

with tab_qr:
    st.markdown("### Gerador de QR Code")

    conteudo_qr = st.text_area(
        "Conteúdo do QR Code",
        placeholder="Digite uma URL, texto, email, telefone...",
        height=120,
        key="qr_conteudo"
    )

    if conteudo_qr:
        st.success("Conteúdo pronto para gerar QR Code.")
    else:
        st.info("Digite algum conteúdo para gerar o preview.")

    st.markdown("#### Preview")
    st.empty()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("Baixar SVG", use_container_width=True, disabled=True, key="qr_svg")

    with col2:
        st.button("Baixar PDF", use_container_width=True, disabled=True, key="qr_pdf")

    with col3:
        st.button("Baixar PNG", use_container_width=True, disabled=True, key="qr_png")

    with st.expander("⚙ Opções avançadas", expanded=False):
        st.slider("Tamanho", 100, 1000, 300)
        st.slider("Margem", 0, 10, 2)
        st.checkbox("Fundo transparente", value=True, key="qr_transparente")
        st.color_picker("Cor do QR Code", "#000000")
        st.color_picker("Cor do fundo", "#FFFFFF", key="qr_fundo")


# =========================
# ABA 3 — LEITOR
# =========================

with tab_reader:
    st.markdown("### Leitor de Código")

    arquivo = st.file_uploader(
        "Envie uma imagem ou PDF",
        type=["png", "jpg", "jpeg", "webp", "pdf"],
        key="leitor_upload"
    )

    if arquivo:
        st.success("Arquivo recebido. A leitura será implementada na próxima etapa.")
    else:
        st.info("Envie um arquivo para tentar identificar EAN-13 ou QR Code.")

    st.markdown("#### Resultado")

    st.write("**Tipo:** —")
    st.write("**Conteúdo:** —")
    st.write("**Informações:** —")