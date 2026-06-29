import streamlit as st
import streamlit.components.v1 as components
import base64
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor

from core.components import titulo_tool


# =========================
# FUNÇÕES — EAN-13
# =========================

L_CODES = {
    "0": "0001101", "1": "0011001", "2": "0010011", "3": "0111101",
    "4": "0100011", "5": "0110001", "6": "0101111", "7": "0111011",
    "8": "0110111", "9": "0001011",
}

G_CODES = {
    "0": "0100111", "1": "0110011", "2": "0011011", "3": "0100001",
    "4": "0011101", "5": "0111001", "6": "0000101", "7": "0010001",
    "8": "0001001", "9": "0010111",
}

R_CODES = {
    "0": "1110010", "1": "1100110", "2": "1101100", "3": "1000010",
    "4": "1011100", "5": "1001110", "6": "1010000", "7": "1000100",
    "8": "1001000", "9": "1110100",
}

PARITY = {
    "0": "LLLLLL", "1": "LLGLGG", "2": "LLGGLG", "3": "LLGGGL",
    "4": "LGLLGG", "5": "LGGLLG", "6": "LGGGLL", "7": "LGLGLG",
    "8": "LGLGGL", "9": "LGGLGL",
}


def calcular_digito_ean13(codigo_12):
    soma = 0
    for i, numero in enumerate(codigo_12):
        digito = int(numero)
        soma += digito if i % 2 == 0 else digito * 3

    resto = soma % 10
    return str(0 if resto == 0 else 10 - resto)


def normalizar_ean13(codigo):
    codigo = codigo.strip()

    if not codigo:
        return None, ""

    if not codigo.isdigit():
        return None, "Digite apenas números."

    if len(codigo) < 12:
        return None, "O EAN-13 precisa ter 12 ou 13 dígitos."

    if len(codigo) > 13:
        return None, "O EAN-13 não pode ter mais de 13 dígitos."

    if len(codigo) == 12:
        digito = calcular_digito_ean13(codigo)
        return codigo + digito, f"Dígito verificador calculado automaticamente: {digito}"

    codigo_12 = codigo[:12]
    digito_correto = calcular_digito_ean13(codigo_12)

    if codigo[-1] == digito_correto:
        return codigo, "Código EAN-13 válido."

    return None, f"Dígito verificador incorreto. O correto seria: {codigo_12 + digito_correto}"


def gerar_pattern_ean13(codigo):
    primeiro = codigo[0]
    esquerda = codigo[1:7]
    direita = codigo[7:13]

    pattern = "101"

    for digito, tipo in zip(esquerda, PARITY[primeiro]):
        pattern += L_CODES[digito] if tipo == "L" else G_CODES[digito]

    pattern += "01010"

    for digito in direita:
        pattern += R_CODES[digito]

    pattern += "101"

    return pattern


def obter_geometria_ean13(largura_mm):
    quiet_zone_mm = 3.63
    area_barras_mm = largura_mm - (quiet_zone_mm * 2)
    modulo_mm = area_barras_mm / 95

    return {
        "quiet_zone_mm": quiet_zone_mm,
        "modulo_mm": modulo_mm,
        "y_barras": 1.0,
        "altura_barras_mm": 17.8,
        "altura_guardas_mm": 21.2,
        "y_texto": 21.90,
        "tamanho_fonte": 3.70,
    }


def obter_guard_positions():
    return set(
        list(range(0, 3)) +
        list(range(45, 50)) +
        list(range(92, 95))
    )


def gerar_barras_svg(pattern, cor_barras, largura_mm):
    geo = obter_geometria_ean13(largura_mm)
    guard_positions = obter_guard_positions()

    rects = []
    x = geo["quiet_zone_mm"]

    for i, bit in enumerate(pattern):
        if bit == "1":
            altura = geo["altura_guardas_mm"] if i in guard_positions else geo["altura_barras_mm"]

            rects.append(
                f'<rect x="{x:.4f}" y="{geo["y_barras"]:.4f}" '
                f'width="{geo["modulo_mm"]:.4f}" height="{altura:.4f}" '
                f'fill="{cor_barras}" />'
            )

        x += geo["modulo_mm"]

    return "\n".join(rects)


def gerar_texto_svg(codigo, cor_barras, largura_mm=37.29):
    geo = obter_geometria_ean13(largura_mm)

    x_inicio_barras = geo["quiet_zone_mm"]
    x_primeiro = geo["quiet_zone_mm"] / 2
    x_bloco_esquerdo = x_inicio_barras + ((3 + 42 / 2) * geo["modulo_mm"])
    x_bloco_direito = x_inicio_barras + ((50 + 42 / 2) * geo["modulo_mm"])

    return f"""
    <text x="{x_primeiro:.4f}" y="{geo["y_texto"]}"
          font-family="Arial, Helvetica, sans-serif"
          font-size="{geo["tamanho_fonte"]}"
          text-anchor="middle"
          fill="{cor_barras}">
        {codigo[0]}
    </text>

    <text x="{x_bloco_esquerdo:.4f}" y="{geo["y_texto"]}"
          font-family="Arial, Helvetica, sans-serif"
          font-size="{geo["tamanho_fonte"]}"
          text-anchor="middle"
          fill="{cor_barras}">
        {codigo[1:7]}
    </text>

    <text x="{x_bloco_direito:.4f}" y="{geo["y_texto"]}"
          font-family="Arial, Helvetica, sans-serif"
          font-size="{geo["tamanho_fonte"]}"
          text-anchor="middle"
          fill="{cor_barras}">
        {codigo[7:13]}
    </text>
    """


def gerar_fundo_svg(cor_fundo):
    if cor_fundo == "transparent":
        return ""

    return f'<rect width="100%" height="100%" fill="{cor_fundo}" />'


def gerar_ean13_svg(
    codigo,
    largura_mm=37.29,
    altura_mm=25.93,
    cor_barras="#000000",
    cor_fundo="transparent",
    mostrar_numeros=True,
    margem_extra_px=1,
):
    pattern = gerar_pattern_ean13(codigo)

    fundo = gerar_fundo_svg(cor_fundo)
    barras = gerar_barras_svg(pattern, cor_barras, largura_mm)
    textos = gerar_texto_svg(codigo, cor_barras, largura_mm) if mostrar_numeros else ""

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{largura_mm}mm"
     height="{altura_mm}mm"
     viewBox="0 0 {largura_mm} {altura_mm}">
    {fundo}

    <g id="EAN13_{codigo}">
        {barras}
        {textos}
    </g>
</svg>
"""

    return svg.encode("utf-8")


def gerar_ean13_pdf(
    codigo,
    largura_mm=37.29,
    altura_mm=25.93,
    cor_barras="#000000",
    cor_fundo="transparent",
    mostrar_numeros=True,
):
    pattern = gerar_pattern_ean13(codigo)
    geo = obter_geometria_ean13(largura_mm)
    guard_positions = obter_guard_positions()

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(largura_mm * mm, altura_mm * mm))

    if cor_fundo != "transparent":
        c.setFillColor(HexColor(cor_fundo))
        c.rect(0, 0, largura_mm * mm, altura_mm * mm, fill=1, stroke=0)

    c.setFillColor(HexColor(cor_barras))

    x = geo["quiet_zone_mm"]

    for i, bit in enumerate(pattern):
        if bit == "1":
            altura = geo["altura_guardas_mm"] if i in guard_positions else geo["altura_barras_mm"]

            c.rect(
                x * mm,
                (altura_mm - geo["y_barras"] - altura) * mm,
                geo["modulo_mm"] * mm,
                altura * mm,
                fill=1,
                stroke=0,
            )

        x += geo["modulo_mm"]

    if mostrar_numeros:
        x_inicio_barras = geo["quiet_zone_mm"]
        x_primeiro = geo["quiet_zone_mm"] / 2
        x_bloco_esquerdo = x_inicio_barras + ((3 + 42 / 2) * geo["modulo_mm"])
        x_bloco_direito = x_inicio_barras + ((50 + 42 / 2) * geo["modulo_mm"])

        c.setFont("Helvetica", geo["tamanho_fonte"] * mm)
        y_pdf = altura_mm - geo["y_texto"]

        c.drawCentredString(x_primeiro * mm, y_pdf * mm, codigo[0])
        c.drawCentredString(x_bloco_esquerdo * mm, y_pdf * mm, codigo[1:7])
        c.drawCentredString(x_bloco_direito * mm, y_pdf * mm, codigo[7:13])

    c.showPage()
    c.save()

    return buffer.getvalue()


def carregar_fonte_png(tamanho_px):
    caminhos = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    for caminho in caminhos:
        try:
            return ImageFont.truetype(caminho, tamanho_px)
        except Exception:
            pass

    return ImageFont.load_default()


def gerar_ean13_png(
    codigo,
    largura_mm=37.29,
    altura_mm=25.93,
    cor_barras="#000000",
    cor_fundo="transparent",
    mostrar_numeros=True,
    dpi=300,
):
    pattern = gerar_pattern_ean13(codigo)
    geo = obter_geometria_ean13(largura_mm)
    guard_positions = obter_guard_positions()

    px_por_mm = dpi / 25.4
    largura_px = int(round(largura_mm * px_por_mm))
    altura_px = int(round(altura_mm * px_por_mm))

    fundo = (255, 255, 255, 0) if cor_fundo == "transparent" else cor_fundo
    imagem = Image.new("RGBA", (largura_px, altura_px), fundo)
    draw = ImageDraw.Draw(imagem)

    x = geo["quiet_zone_mm"]

    for i, bit in enumerate(pattern):
        if bit == "1":
            altura = geo["altura_guardas_mm"] if i in guard_positions else geo["altura_barras_mm"]

            x0 = int(round(x * px_por_mm))
            y0 = int(round(geo["y_barras"] * px_por_mm))
            x1 = int(round((x + geo["modulo_mm"]) * px_por_mm))
            y1 = int(round((geo["y_barras"] + altura) * px_por_mm))

            draw.rectangle([x0, y0, x1, y1], fill=cor_barras)

        x += geo["modulo_mm"]

    if mostrar_numeros:
        fonte = carregar_fonte_png(int(round(geo["tamanho_fonte"] * px_por_mm)))

        x_inicio_barras = geo["quiet_zone_mm"]
        x_primeiro = geo["quiet_zone_mm"] / 2
        x_bloco_esquerdo = x_inicio_barras + ((3 + 42 / 2) * geo["modulo_mm"])
        x_bloco_direito = x_inicio_barras + ((50 + 42 / 2) * geo["modulo_mm"])

        y = int(round((geo["y_texto"] - geo["tamanho_fonte"]) * px_por_mm))

        for texto, x_mm in [
            (codigo[0], x_primeiro),
            (codigo[1:7], x_bloco_esquerdo),
            (codigo[7:13], x_bloco_direito),
        ]:
            bbox = draw.textbbox((0, 0), texto, font=fonte)
            texto_largura = bbox[2] - bbox[0]
            draw.text(
                (int(round(x_mm * px_por_mm - texto_largura / 2)), y),
                texto,
                fill=cor_barras,
                font=fonte,
            )

    buffer = BytesIO()
    imagem.save(buffer, format="PNG", dpi=(dpi, dpi))
    return buffer.getvalue()


def svg_para_base64(svg_bytes):
    return base64.b64encode(svg_bytes).decode("utf-8")


# =========================
# INTERFACE
# =========================

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
    st.markdown("### Gerador EAN-13")

    codigo_ean = st.text_input(
        "Digite 12 ou 13 dígitos para gerar o preview",
        placeholder="Ex.: 590123412345",
        max_chars=13,
        key="ean_codigo"
    ).strip()

    ean_final = None
    svg_ean = None
    pdf_ean = None
    png_ean = None

    ean_final, mensagem = normalizar_ean13(codigo_ean) if codigo_ean else (None, "")

    with st.expander("⚙ Opções avançadas"):
        altura_barras = st.slider("Altura visual das barras", 10, 80, 26)
        escala = st.slider("Escala", 80, 150, 100)
        mostrar_numeros = st.checkbox("Mostrar números", value=True)
        fundo_transparente = st.checkbox("Fundo transparente", value=True)
        cor_barras = st.color_picker("Cor das barras", "#000000")
        cor_fundo_picker = st.color_picker("Cor de fundo", "#FFFFFF")
        margem_adicional = st.number_input("Margem adicional (px)", min_value=0, max_value=20, value=1)

    if codigo_ean:
        if ean_final:
            st.success(mensagem)

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
                margem_extra_px=margem_adicional,
            )

            pdf_ean = gerar_ean13_pdf(
                ean_final,
                largura_mm=largura_final,
                altura_mm=altura_final,
                cor_barras=cor_barras,
                cor_fundo=cor_fundo,
                mostrar_numeros=mostrar_numeros,
            )

            png_ean = gerar_ean13_png(
                ean_final,
                largura_mm=largura_final,
                altura_mm=altura_final,
                cor_barras=cor_barras,
                cor_fundo=cor_fundo,
                mostrar_numeros=mostrar_numeros,
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