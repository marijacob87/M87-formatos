import base64
from io import BytesIO

import segno


def gerar_qrcode_svg(
    conteudo,
    cor_qr="#000000",
    cor_fundo="transparent",
    margem=2,
    escala=8,
):
    qr = segno.make(conteudo, error="h")

    buffer = BytesIO()

    qr.save(
        buffer,
        kind="svg",
        scale=escala,
        border=margem,
        dark=cor_qr,
        light=None if cor_fundo == "transparent" else cor_fundo,
    )

    return buffer.getvalue()


def gerar_qrcode_png(
    conteudo,
    cor_qr="#000000",
    cor_fundo="transparent",
    margem=2,
    escala=12,
    dpi=300,
):
    qr = segno.make(conteudo, error="h")

    buffer = BytesIO()

    qr.save(
        buffer,
        kind="png",
        scale=escala,
        border=margem,
        dark=cor_qr,
        light=None if cor_fundo == "transparent" else cor_fundo,
        dpi=dpi,
    )

    return buffer.getvalue()


def gerar_qrcode_pdf(
    conteudo,
    cor_qr="#000000",
    cor_fundo="transparent",
    margem=2,
    escala=8,
):
    qr = segno.make(conteudo, error="h")

    buffer = BytesIO()

    qr.save(
        buffer,
        kind="pdf",
        scale=escala,
        border=margem,
        dark=cor_qr,
        light=None if cor_fundo == "transparent" else cor_fundo,
    )

    return buffer.getvalue()


def arquivo_para_base64(arquivo_bytes):
    return base64.b64encode(arquivo_bytes).decode("utf-8")