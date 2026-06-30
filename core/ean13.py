import base64
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor


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


def obter_geometria_ean13(largura_mm, altura_barras_visual=26):
    quiet_zone_mm = 3.63
    area_barras_mm = largura_mm - (quiet_zone_mm * 2)
    modulo_mm = area_barras_mm / 95

    fator = altura_barras_visual / 26

    return {
        "quiet_zone_mm": quiet_zone_mm,
        "modulo_mm": modulo_mm,
        "y_barras": 1.0,
        "altura_barras_mm": 17.8 * fator,
        "altura_guardas_mm": 21.2 * fator,
        "y_texto": 21.90 * fator,
        "tamanho_fonte": 3.70 * fator,
    }


def obter_guard_positions():
    return set(
        list(range(0, 3)) +
        list(range(45, 50)) +
        list(range(92, 95))
    )


def gerar_fundo_svg(cor_fundo, largura_total, altura_total):
    if cor_fundo == "transparent":
        return ""

    return f'<rect width="{largura_total}" height="{altura_total}" fill="{cor_fundo}" />'


def gerar_barras_svg(pattern, cor_barras, largura_mm, margem_mm, altura_barras_visual):
    geo = obter_geometria_ean13(largura_mm, altura_barras_visual)
    guard_positions = obter_guard_positions()

    rects = []
    x = geo["quiet_zone_mm"] + margem_mm
    y = geo["y_barras"] + margem_mm

    for i, bit in enumerate(pattern):
        if bit == "1":
            altura = geo["altura_guardas_mm"] if i in guard_positions else geo["altura_barras_mm"]

            rects.append(
                f'<rect x="{x:.4f}" y="{y:.4f}" '
                f'width="{geo["modulo_mm"]:.4f}" height="{altura:.4f}" '
                f'fill="{cor_barras}" />'
            )

        x += geo["modulo_mm"]

    return "\n".join(rects)


def gerar_texto_svg(codigo, cor_barras, largura_mm, margem_mm, altura_barras_visual):
    geo = obter_geometria_ean13(largura_mm, altura_barras_visual)

    x_inicio_barras = geo["quiet_zone_mm"] + margem_mm
    x_primeiro = (geo["quiet_zone_mm"] / 2) + margem_mm
    x_bloco_esquerdo = x_inicio_barras + ((3 + 42 / 2) * geo["modulo_mm"])
    x_bloco_direito = x_inicio_barras + ((50 + 42 / 2) * geo["modulo_mm"])

    y_texto = geo["y_texto"] + margem_mm

    return f"""
    <text x="{x_primeiro:.4f}" y="{y_texto:.4f}"
          font-family="Arial, Helvetica, sans-serif"
          font-size="{geo["tamanho_fonte"]:.4f}"
          text-anchor="middle"
          fill="{cor_barras}">{codigo[0]}</text>

    <text x="{x_bloco_esquerdo:.4f}" y="{y_texto:.4f}"
          font-family="Arial, Helvetica, sans-serif"
          font-size="{geo["tamanho_fonte"]:.4f}"
          text-anchor="middle"
          fill="{cor_barras}">{codigo[1:7]}</text>

    <text x="{x_bloco_direito:.4f}" y="{y_texto:.4f}"
          font-family="Arial, Helvetica, sans-serif"
          font-size="{geo["tamanho_fonte"]:.4f}"
          text-anchor="middle"
          fill="{cor_barras}">{codigo[7:13]}</text>
    """


def gerar_ean13_svg(
    codigo,
    largura_mm=37.29,
    altura_mm=25.93,
    cor_barras="#000000",
    cor_fundo="transparent",
    mostrar_numeros=True,
    margem_adicional_mm=0,
    altura_barras_visual=26,
):
    pattern = gerar_pattern_ean13(codigo)

    largura_total = largura_mm + (margem_adicional_mm * 2)
    altura_total = altura_mm + (margem_adicional_mm * 2)

    fundo = gerar_fundo_svg(cor_fundo, largura_total, altura_total)
    barras = gerar_barras_svg(
        pattern,
        cor_barras,
        largura_mm,
        margem_adicional_mm,
        altura_barras_visual,
    )
    textos = (
        gerar_texto_svg(
            codigo,
            cor_barras,
            largura_mm,
            margem_adicional_mm,
            altura_barras_visual,
        )
        if mostrar_numeros
        else ""
    )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{largura_total}mm"
     height="{altura_total}mm"
     viewBox="0 0 {largura_total} {altura_total}">
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
    margem_adicional_mm=0,
    altura_barras_visual=26,
):
    pattern = gerar_pattern_ean13(codigo)
    geo = obter_geometria_ean13(largura_mm, altura_barras_visual)
    guard_positions = obter_guard_positions()

    largura_total = largura_mm + (margem_adicional_mm * 2)
    altura_total = altura_mm + (margem_adicional_mm * 2)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(largura_total * mm, altura_total * mm))

    if cor_fundo != "transparent":
        c.setFillColor(HexColor(cor_fundo))
        c.rect(0, 0, largura_total * mm, altura_total * mm, fill=1, stroke=0)

    c.setFillColor(HexColor(cor_barras))

    x = geo["quiet_zone_mm"] + margem_adicional_mm

    for i, bit in enumerate(pattern):
        if bit == "1":
            altura = geo["altura_guardas_mm"] if i in guard_positions else geo["altura_barras_mm"]

            c.rect(
                x * mm,
                (altura_total - margem_adicional_mm - geo["y_barras"] - altura) * mm,
                geo["modulo_mm"] * mm,
                altura * mm,
                fill=1,
                stroke=0,
            )

        x += geo["modulo_mm"]

    if mostrar_numeros:
        x_inicio_barras = geo["quiet_zone_mm"] + margem_adicional_mm
        x_primeiro = (geo["quiet_zone_mm"] / 2) + margem_adicional_mm
        x_bloco_esquerdo = x_inicio_barras + ((3 + 42 / 2) * geo["modulo_mm"])
        x_bloco_direito = x_inicio_barras + ((50 + 42 / 2) * geo["modulo_mm"])

        c.setFont("Helvetica", geo["tamanho_fonte"] * mm)
        y_pdf = altura_total - margem_adicional_mm - geo["y_texto"]

        c.drawCentredString(x_primeiro * mm, y_pdf * mm, codigo[0])
        c.drawCentredString(x_bloco_esquerdo * mm, y_pdf * mm, codigo[1:7])
        c.drawCentredString(x_bloco_direito * mm, y_pdf * mm, codigo[7:13])

    c.showPage()
    c.save()

    return buffer.getvalue()


def carregar_fonte_png(tamanho_px):
    caminhos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
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
    margem_adicional_mm=0,
    altura_barras_visual=26,
    dpi=300,
):
    pattern = gerar_pattern_ean13(codigo)
    geo = obter_geometria_ean13(largura_mm, altura_barras_visual)
    guard_positions = obter_guard_positions()

    largura_total = largura_mm + (margem_adicional_mm * 2)
    altura_total = altura_mm + (margem_adicional_mm * 2)

    px_por_mm = dpi / 25.4
    largura_px = int(round(largura_total * px_por_mm))
    altura_px = int(round(altura_total * px_por_mm))

    fundo = (255, 255, 255, 0) if cor_fundo == "transparent" else cor_fundo
    imagem = Image.new("RGBA", (largura_px, altura_px), fundo)
    draw = ImageDraw.Draw(imagem)

    x = geo["quiet_zone_mm"] + margem_adicional_mm

    for i, bit in enumerate(pattern):
        if bit == "1":
            altura = geo["altura_guardas_mm"] if i in guard_positions else geo["altura_barras_mm"]

            x0 = int(round(x * px_por_mm))
            y0 = int(round((geo["y_barras"] + margem_adicional_mm) * px_por_mm))
            x1 = int(round((x + geo["modulo_mm"]) * px_por_mm))
            y1 = int(round((geo["y_barras"] + margem_adicional_mm + altura) * px_por_mm))

            draw.rectangle([x0, y0, x1, y1], fill=cor_barras)

        x += geo["modulo_mm"]

    if mostrar_numeros:
        fonte = carregar_fonte_png(int(round(geo["tamanho_fonte"] * px_por_mm)))

        x_inicio_barras = geo["quiet_zone_mm"] + margem_adicional_mm
        x_primeiro = (geo["quiet_zone_mm"] / 2) + margem_adicional_mm
        x_bloco_esquerdo = x_inicio_barras + ((3 + 42 / 2) * geo["modulo_mm"])
        x_bloco_direito = x_inicio_barras + ((50 + 42 / 2) * geo["modulo_mm"])

        y = int(round((geo["y_texto"] - geo["tamanho_fonte"] + 1 + margem_adicional_mm) * px_por_mm))

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