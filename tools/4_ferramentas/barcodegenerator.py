import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image
from streamlit_paste_button import paste_image_button

from core.components import titulo_tool

from core.ean13 import (
    normalizar_ean13,
    gerar_ean13_svg,
    gerar_ean13_pdf,
    gerar_ean13_png,
    svg_para_base64,
)

from core.qrcode_m87 import (
    gerar_qrcode_svg,
    gerar_qrcode_pdf,
    gerar_qrcode_png,
    arquivo_para_base64,
)


# =========================
# CONFIGURAÇÃO INICIAL
# =========================



# =========================
# CSS
# =========================

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

        .m87-help-text {
            color: rgba(255,255,255,.62);
            font-size: .90rem;
            line-height: 1.5;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# SESSION STATE
# =========================

def iniciar_session_state():
    valores_iniciais = {
        "qr_svg": None,
        "qr_pdf": None,
        "qr_png": None,
        "qr_nome": "QRCode_M87",
    }

    for chave, valor in valores_iniciais.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


iniciar_session_state()


# =========================
# COMPONENTES VISUAIS
# =========================

def texto_info(texto):
    st.markdown(
        f"""
        <div class="m87-help-text">
            {texto}
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_preview_svg(svg_bytes, largura_px=660, padding_px=12, mensagem_vazia="Digite um conteúdo para gerar o preview."):
    if not svg_bytes:
        st.info(mensagem_vazia)
        return

    svg_base64 = svg_para_base64(svg_bytes)

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
                    padding: {padding_px}px;
                    width: {largura_px}px;
                    max-width: 100%;
                    height: auto;
                ">
        </div>
        """,
        height=430,
    )


def botoes_download(svg_bytes, pdf_bytes, png_bytes, nome_base):
    st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)

    st.download_button(
        "⬇  Baixar SVG",
        data=svg_bytes if svg_bytes else b"",
        file_name=f"{nome_base}.svg",
        mime="image/svg+xml",
        use_container_width=True,
        type="secondary",
        disabled=not bool(svg_bytes),
    )

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    st.download_button(
        "⬇  Baixar PDF",
        data=pdf_bytes if pdf_bytes else b"",
        file_name=f"{nome_base}.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="secondary",
        disabled=not bool(pdf_bytes),
    )

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    st.download_button(
        "⬇  Baixar PNG",
        data=png_bytes if png_bytes else b"",
        file_name=f"{nome_base}.png",
        mime="image/png",
        use_container_width=True,
        type="secondary",
        disabled=not bool(png_bytes),
    )


# =========================
# ABA EAN-13
# =========================

def aba_ean13():
    texto_info("Digite 12 dígitos para que o 13º seja calculado automaticamente.")

    codigo_ean = st.text_input(
        "",
        max_chars=13,
        key="ean_codigo",
        label_visibility="collapsed",
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
        mostrar_preview_svg(
            svg_ean,
            largura_px=660,
            padding_px=12,
            mensagem_vazia="Digite um EAN-13 válido para ver o preview.",
        )

    with col_download:
        nome_base = f"EAN13_{ean_final}" if ean_final else "EAN13"
        botoes_download(svg_ean, pdf_ean, png_ean, nome_base)


# =========================
# ABA QR CODE
# =========================

def aba_qrcode():
    texto_info(
        "Gere QR Codes para sites, links, textos, contatos, telefones, emails, "
        "endereços, redes sociais, Wi-Fi, instruções rápidas ou qualquer informação em texto."
    )

    conteudo_qr = st.text_area(
        "",
        placeholder="Cole aqui um link, texto, email, telefone, contato...",
        height=120,
        key="qr_conteudo",
        label_visibility="collapsed",
    ).strip()

    with st.expander("⚙ Opções avançadas", expanded=False):
        col_qr1, col_qr2 = st.columns(2)

        with col_qr1:
            escala_qr = st.slider(
                "Escala",
                min_value=4,
                max_value=20,
                value=8,
                key="qr_escala"
            )

            margem_qr = st.slider(
                "Margem",
                min_value=0,
                max_value=10,
                value=2,
                key="qr_margem"
            )

        with col_qr2:
            cor_qr = st.color_picker(
                "Cor do QR Code",
                "#000000",
                key="qr_cor"
            )

            fundo_qr_transparente = st.checkbox(
                "Fundo transparente",
                value=True,
                key="qr_fundo_transparente"
            )

            cor_fundo_qr_picker = st.color_picker(
                "Cor de fundo",
                "#FFFFFF",
                key="qr_fundo_cor",
                disabled=fundo_qr_transparente
            )

    gerar_qr = st.button(
        "Gerar QR Code",
        use_container_width=True,
        type="primary",
        disabled=not bool(conteudo_qr),
    )

    if gerar_qr and conteudo_qr:
        cor_fundo_qr = "transparent" if fundo_qr_transparente else cor_fundo_qr_picker

        st.session_state.qr_svg = gerar_qrcode_svg(
            conteudo_qr,
            cor_qr=cor_qr,
            cor_fundo=cor_fundo_qr,
            margem=margem_qr,
            escala=escala_qr,
        )

        st.session_state.qr_pdf = gerar_qrcode_pdf(
            conteudo_qr,
            cor_qr=cor_qr,
            cor_fundo=cor_fundo_qr,
            margem=margem_qr,
            escala=escala_qr,
        )

        st.session_state.qr_png = gerar_qrcode_png(
            conteudo_qr,
            cor_qr=cor_qr,
            cor_fundo=cor_fundo_qr,
            margem=margem_qr,
            escala=escala_qr + 4,
        )

        st.session_state.qr_nome = "QRCode_M87"

    qr_svg = st.session_state.qr_svg
    qr_pdf = st.session_state.qr_pdf
    qr_png = st.session_state.qr_png
    qr_nome = st.session_state.qr_nome

    st.markdown("#### Preview")

    col_preview_qr, col_download_qr = st.columns([3.85, 1.65], gap="large")

    with col_preview_qr:
        if qr_svg:
            qr_base64 = arquivo_para_base64(qr_svg)

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
                        src="data:image/svg+xml;base64,{qr_base64}"
                        style="
                            background: white;
                            padding: 18px;
                            width: 320px;
                            max-width: 100%;
                            height: auto;
                        ">
                </div>
                """,
                height=430,
            )
        else:
            st.info("Digite um conteúdo e clique em **Gerar QR Code**.")

    with col_download_qr:
        botoes_download(qr_svg, qr_pdf, qr_png, qr_nome)

def ler_codigo_imagem(imagem):
    imagem_rgb = imagem.convert("RGB")
    imagem_np = np.array(imagem_rgb)

    detector = cv2.QRCodeDetector()
    conteudo, pontos, _ = detector.detectAndDecode(imagem_np)

    if conteudo:
        return {
            "tipo": "QR Code",
            "conteudo": conteudo,
            "informacoes": "Leitura feita com OpenCV."
        }

    return None



# =========================
# ABA LEITOR
# =========================

def aba_leitor():
    texto_info("Envie uma imagem, PDF ou cole um print para identificar automaticamente EAN-13 ou QR Code.")

    modo_leitor = st.radio(
        "Entrada",
        ["Upload", "Colar print"],
        horizontal=True,
        label_visibility="collapsed",
    )

    resultado = None

    if modo_leitor == "Upload":
        arquivo = st.file_uploader(
            "",
            type=["png", "jpg", "jpeg", "webp", "pdf"],
            key="leitor_upload",
            label_visibility="collapsed",
        )

        if arquivo:
            try:
                imagem = Image.open(arquivo).convert("RGB")

                st.image(
                    imagem,
                    caption="Imagem enviada",
                    width=380,
                )

                resultado = ler_codigo_imagem(imagem)

                

            except Exception as erro:
                st.error("Não consegui ler esse arquivo como imagem.")
                st.code(str(erro))
        else:
            st.info("Envie uma imagem para tentar identificar o código.")

    else:
        imagem_colada = paste_image_button(
            label="📋 Colar imagem do clipboard",
        )

        if imagem_colada.image_data is not None:
            imagem = imagem_colada.image_data.convert("RGB")

            st.image(
                imagem,
                caption="Imagem colada",
                width=380,
            )

            resultado = ler_codigo_imagem(imagem)

     
        else:
            st.info("Copie um print e clique no botão para colar.")

    
    if resultado:
        st.write(f"**Tipo:** {resultado['tipo']}")
        st.write(f"**Conteúdo:** {resultado['conteudo']}")
        
    else:
        st.write("**Tipo:** —")
        st.write("**Conteúdo:** —")
        


# =========================
# TABS
# =========================

tab_ean, tab_qr, tab_reader = st.tabs(
    ["EAN-13", "QR CODE", "LEITOR DE CÓDIGO"]
)

with tab_ean:
    aba_ean13()

with tab_qr:
    aba_qrcode()

with tab_reader:
    aba_leitor()