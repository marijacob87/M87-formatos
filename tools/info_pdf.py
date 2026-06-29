import re
from datetime import datetime
from io import BytesIO
from html import escape

import fitz
import pikepdf
import streamlit as st

from core.components import titulo_tool


MM_PER_POINT = 25.4 / 72
POINT_PER_MM = 72 / 25.4

PROCESS_COLORS = {
    "Cyan": "C",
    "C": "C",
    "Magenta": "M",
    "M": "M",
    "Yellow": "Y",
    "Y": "Y",
    "Black": "K",
    "K": "K",
}

IGNORE_SPOT_NAMES = {"All", "None", "Registration"}


titulo_tool("Info PDF")


st.markdown(
    """
    <style>
        .info-label {
            font-size: 0.68rem;
            font-weight: 900;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.48);
            line-height: 1.1;
            margin-bottom: 2px;
        }

        .info-value {
            font-size: 0.92rem;
            font-weight: 500;
            color: rgba(255,255,255,0.88);
            line-height: 1.25;
        }

        .info-row {
            margin-bottom: 10px;
        }

        .info-note {
            font-size: 0.78rem;
            line-height: 1.35;
            color: rgba(255,255,255,0.72);
            background: rgba(208,147,29,0.10);
            border-left: 3px solid rgba(208,147,29,0.75);
            padding: 8px 10px;
            border-radius: 8px;
            margin: 8px 0 12px 0;
        }

        .section-line {
            height: 1px;
            background: rgba(255,255,255,0.07);
            margin: 16px 0 14px 0;
        }

        .preview-caption {
            color: rgba(255,255,255,0.55);
            font-size: 0.76rem;
            text-align: center;
            margin-top: 6px;
        }

        .separacoes-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px 34px;
            margin-top: 4px;
            margin-bottom: 12px;
        }

        .separacoes-col {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .cor-item {
            display: flex;
            align-items: center;
            gap: 8px;
            color: rgba(255,255,255,0.84);
            font-size: 0.88rem;
            font-weight: 500;
        }

        .cor-box {
            width: 14px;
            height: 14px;
            border-radius: 4px;
            border: 1px solid rgba(208,147,29,0.70);
            background: transparent;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #0E1117;
            font-size: 10px;
            font-weight: 900;
            line-height: 1;
        }

        .cor-box.ativo {
            background: #D0931D;
            border-color: #D0931D;
        }

        .rgb-alerta {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 17px;
            height: 17px;
            margin-left: 6px;
            border-radius: 50%;
            background: #D0931D;
            color: #0E1117;
            font-size: 12px;
            font-weight: 900;
            animation: m87-pisca-alerta 0.9s infinite;
        }

        @keyframes m87-pisca-alerta {
            0%, 100% {
                opacity: 1;
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(208,147,29,0.65);
            }
            50% {
                opacity: 0.45;
                transform: scale(1.12);
                box-shadow: 0 0 0 7px rgba(208,147,29,0);
            }
        }

        .pantone-lista {
            color: rgba(255,255,255,0.88);
            font-size: 0.88rem;
            font-weight: 500;
            line-height: 1.6;
            margin-top: 2px;
            margin-bottom: 10px;
        }

        [data-testid="stFileUploader"] {
            background: rgba(31, 41, 55, 0.38);
            border: 1px dashed rgba(208,147,29,0.45);
            border-radius: 14px;
            padding: 10px;
            margin-bottom: 10px;
        }

        [data-testid="stFileUploader"] section {
            padding: 10px !important;
        }

        [data-testid="stFileUploader"] small {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def pt_to_mm(valor):
    return round(float(valor) * MM_PER_POINT, 2)


def mm_to_pt(valor):
    return float(valor) * POINT_PER_MM


def box_to_mm(box):
    largura_pt = float(box[2]) - float(box[0])
    altura_pt = float(box[3]) - float(box[1])
    return pt_to_mm(largura_pt), pt_to_mm(altura_pt)


def formatar_mm(largura, altura):
    return f"{largura:.1f} mm x {altura:.1f} mm"


def orientacao(largura, altura):
    if abs(largura - altura) < 0.5:
        return "Quadrado"
    if largura > altura:
        return "Paisagem"
    return "Retrato"


def formatar_data_pdf(data_pdf):
    if not data_pdf:
        return "Não informado"

    try:
        limpa = data_pdf.replace("D:", "")
        data = datetime.strptime(limpa[:14], "%Y%m%d%H%M%S")
        return data.strftime("%d/%m/%Y às %H:%M")
    except Exception:
        return data_pdf


def formatar_peso(bytes_total):
    if bytes_total < 1024 * 1024:
        return f"{bytes_total / 1024:.1f} KB"
    return f"{bytes_total / (1024 * 1024):.2f} MB"


def linha(label, valor):
    st.markdown(
        f"""
        <div class="info-row">
            <div class="info-label">{escape(str(label))}</div>
            <div class="info-value">{escape(str(valor))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def nota(texto):
    st.markdown(
        f'<div class="info-note">⚠️ {escape(str(texto))}</div>',
        unsafe_allow_html=True
    )


def separador():
    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )


def checkbox_visual(label, ativo):
    classe = "cor-box ativo" if ativo else "cor-box"
    check = "✓" if ativo else ""

    return (
        f'<div class="cor-item">'
        f'<span class="{classe}">{check}</span>'
        f'<span>{label}</span>'
        f'</div>'
    )


def mostrar_separacoes(cores):
    st.markdown(
        '<div class="info-label">Separações detectadas</div>',
        unsafe_allow_html=True
    )

    rgb_label = 'RGB <span class="rgb-alerta">!</span>' if cores["RGB"] else "RGB"

    html = (
        '<div class="separacoes-grid">'
        '<div class="separacoes-col">'
        f'{checkbox_visual("Ciano", cores["C"])}'
        f'{checkbox_visual("Magenta", cores["M"])}'
        f'{checkbox_visual("Amarelo", cores["Y"])}'
        f'{checkbox_visual("Preto", cores["K"])}'
        '</div>'
        '<div class="separacoes-col">'
        f'{checkbox_visual(rgb_label, cores["RGB"])}'
        f'{checkbox_visual("Pantones / especiais", bool(cores["SPOTS"]))}'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

    st.markdown(
        '<div class="info-label">Pantones / cores especiais</div>',
        unsafe_allow_html=True
    )

    if cores["SPOTS"]:
        lista_pantones = "<br>".join(
            escape(cor) for cor in cores["SPOTS"]
        )

        st.markdown(
            f'<div class="pantone-lista">{lista_pantones}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="pantone-lista">Nenhuma detectada</div>',
            unsafe_allow_html=True
        )


def analisar_boxes(pdf_bytes):
    paginas = []

    with pikepdf.open(BytesIO(pdf_bytes)) as pdf:
        for numero, pagina in enumerate(pdf.pages, start=1):
            media = pagina.get("/MediaBox")
            trim = pagina.get("/TrimBox")
            bleed = pagina.get("/BleedBox")
            crop = pagina.get("/CropBox")

            media_mm = box_to_mm(media)
            trim_mm = box_to_mm(trim) if trim else media_mm
            bleed_mm = box_to_mm(bleed) if bleed else media_mm
            crop_mm = box_to_mm(crop) if crop else media_mm

            paginas.append(
                {
                    "pagina": numero,
                    "media": media_mm,
                    "trim": trim_mm,
                    "bleed": bleed_mm,
                    "crop": crop_mm,
                    "tem_trim": trim is not None,
                    "tem_bleed": bleed is not None,
                    "tem_crop": crop is not None,
                }
            )

    return paginas


def nome_pdf_para_texto(nome):
    nome = str(nome).replace("/", "")

    def trocar_hex(match):
        try:
            return chr(int(match.group(1), 16))
        except Exception:
            return ""

    return re.sub(r"#([0-9A-Fa-f]{2})", trocar_hex, nome).strip()


def marcar_processo(nome_cor, resultado):
    nome_cor = nome_pdf_para_texto(nome_cor)

    if nome_cor in PROCESS_COLORS:
        canal = PROCESS_COLORS[nome_cor]
        resultado[canal] = True
        resultado["CMYK"] = True
        return

    if nome_cor and nome_cor not in IGNORE_SPOT_NAMES:
        resultado["SPOTS"].add(nome_cor)


def marcar_cmyk(c, m, y, k, resultado):
    if c > 0:
        resultado["C"] = True
    if m > 0:
        resultado["M"] = True
    if y > 0:
        resultado["Y"] = True
    if k > 0:
        resultado["K"] = True

    if c > 0 or m > 0 or y > 0 or k > 0:
        resultado["CMYK"] = True


def analisar_color_space(color_space, resultado, mapa_cores=None):
    try:
        if isinstance(color_space, pikepdf.Name):
            nome = nome_pdf_para_texto(color_space)

            if nome == "DeviceCMYK":
                resultado["CMYK"] = True
            elif nome == "DeviceRGB":
                resultado["RGB"] = True
            elif nome == "DeviceGray":
                resultado["GRAY"] = True

        elif isinstance(color_space, pikepdf.Array) and len(color_space) > 0:
            tipo = nome_pdf_para_texto(color_space[0])

            if tipo == "Separation" and len(color_space) >= 3:
                nome_cor = nome_pdf_para_texto(color_space[1])
                marcar_processo(nome_cor, resultado)
                analisar_color_space(color_space[2], resultado, mapa_cores)

            elif tipo == "DeviceN" and len(color_space) >= 3:
                nomes = color_space[1]

                if isinstance(nomes, pikepdf.Array):
                    for item in nomes:
                        marcar_processo(nome_pdf_para_texto(item), resultado)

                analisar_color_space(color_space[2], resultado, mapa_cores)

            else:
                texto = str(color_space)

                if "DeviceCMYK" in texto:
                    resultado["CMYK"] = True
                if "DeviceRGB" in texto:
                    resultado["RGB"] = True
                if "DeviceGray" in texto:
                    resultado["GRAY"] = True

    except Exception:
        pass


def coletar_mapa_cores(recursos, mapa_cores, resultado, visitados=None):
    if visitados is None:
        visitados = set()

    if recursos is None:
        return

    try:
        obj_id = id(recursos)
        if obj_id in visitados:
            return
        visitados.add(obj_id)

        color_spaces = recursos.get("/ColorSpace", {})

        if isinstance(color_spaces, pikepdf.Dictionary):
            for nome, color_space in color_spaces.items():
                chave = nome_pdf_para_texto(nome)
                mapa_cores[chave] = color_space
                analisar_color_space(color_space, resultado, mapa_cores)

        xobjects = recursos.get("/XObject", {})

        if isinstance(xobjects, pikepdf.Dictionary):
            for _, xobj in xobjects.items():
                try:
                    sub_recursos = xobj.get("/Resources")
                    coletar_mapa_cores(sub_recursos, mapa_cores, resultado, visitados)
                except Exception:
                    pass

    except Exception:
        pass


def tokenizar_pdf_stream(texto):
    padrao = re.compile(
        r"/[^\s\[\]\(\)<>/%]+|"
        r"-?\d*\.?\d+(?:[eE][+-]?\d+)?|"
        r"[A-Za-z\*]+|"
        r"\[|\]"
    )
    return padrao.findall(texto)


def resolver_color_space(nome, mapa_cores):
    nome = nome_pdf_para_texto(nome)

    if nome in ["DeviceCMYK", "DeviceRGB", "DeviceGray"]:
        return nome

    return mapa_cores.get(nome)


def analisar_scn(valores, color_space_atual, mapa_cores, resultado):
    cs = resolver_color_space(color_space_atual, mapa_cores)

    if not cs:
        return

    if isinstance(cs, str):
        if cs == "DeviceCMYK" and len(valores) >= 4:
            marcar_cmyk(valores[-4], valores[-3], valores[-2], valores[-1], resultado)

        elif cs == "DeviceRGB" and len(valores) >= 3:
            if valores[-3] > 0 or valores[-2] > 0 or valores[-1] > 0:
                resultado["RGB"] = True

        elif cs == "DeviceGray" and len(valores) >= 1:
            if valores[-1] > 0:
                resultado["GRAY"] = True

        return

    try:
        if isinstance(cs, pikepdf.Array) and len(cs) > 0:
            tipo = nome_pdf_para_texto(cs[0])

            if tipo == "Separation" and len(cs) >= 2:
                nome_cor = nome_pdf_para_texto(cs[1])
                tint = valores[-1] if valores else 0

                if tint > 0:
                    marcar_processo(nome_cor, resultado)

            elif tipo == "DeviceN" and len(cs) >= 2:
                nomes = cs[1]

                if isinstance(nomes, pikepdf.Array):
                    usados = valores[-len(nomes):]

                    for nome_cor, tint in zip(nomes, usados):
                        if tint > 0:
                            marcar_processo(nome_pdf_para_texto(nome_cor), resultado)

            elif tipo == "ICCBased":
                texto = str(cs)

                if "DeviceCMYK" in texto and len(valores) >= 4:
                    marcar_cmyk(valores[-4], valores[-3], valores[-2], valores[-1], resultado)
                elif "DeviceRGB" in texto and len(valores) >= 3:
                    if valores[-3] > 0 or valores[-2] > 0 or valores[-1] > 0:
                        resultado["RGB"] = True
                elif "DeviceGray" in texto and len(valores) >= 1:
                    if valores[-1] > 0:
                        resultado["GRAY"] = True

    except Exception:
        pass


def analisar_stream_pdf(conteudo, mapa_cores, resultado):
    texto = conteudo.decode("latin-1", errors="ignore")
    tokens = tokenizar_pdf_stream(texto)

    operandos = []
    cs_fill = "DeviceGray"
    cs_stroke = "DeviceGray"

    operadores = {
        "k", "K", "rg", "RG", "g", "G",
        "cs", "CS", "sc", "SC", "scn", "SCN"
    }

    for token in tokens:
        if token not in operadores:
            operandos.append(token)
            continue

        try:
            if token == "k" and len(operandos) >= 4:
                valores = [float(v) for v in operandos[-4:]]
                marcar_cmyk(*valores, resultado)

            elif token == "K" and len(operandos) >= 4:
                valores = [float(v) for v in operandos[-4:]]
                marcar_cmyk(*valores, resultado)

            elif token == "rg" and len(operandos) >= 3:
                r, g, b = [float(v) for v in operandos[-3:]]
                if r > 0 or g > 0 or b > 0:
                    resultado["RGB"] = True

            elif token == "RG" and len(operandos) >= 3:
                r, g, b = [float(v) for v in operandos[-3:]]
                if r > 0 or g > 0 or b > 0:
                    resultado["RGB"] = True

            elif token == "g" and len(operandos) >= 1:
                gray = float(operandos[-1])
                if gray > 0:
                    resultado["GRAY"] = True

            elif token == "G" and len(operandos) >= 1:
                gray = float(operandos[-1])
                if gray > 0:
                    resultado["GRAY"] = True

            elif token == "cs" and operandos:
                cs_fill = nome_pdf_para_texto(operandos[-1])

            elif token == "CS" and operandos:
                cs_stroke = nome_pdf_para_texto(operandos[-1])

            elif token in ["sc", "scn"]:
                valores = [
                    float(v) for v in operandos
                    if re.fullmatch(r"-?\d*\.?\d+(?:[eE][+-]?\d+)?", v)
                ]
                analisar_scn(valores, cs_fill, mapa_cores, resultado)

            elif token in ["SC", "SCN"]:
                valores = [
                    float(v) for v in operandos
                    if re.fullmatch(r"-?\d*\.?\d+(?:[eE][+-]?\d+)?", v)
                ]
                analisar_scn(valores, cs_stroke, mapa_cores, resultado)

        except Exception:
            pass

        operandos = []


def ler_bytes_conteudo_pagina(pagina):
    conteudos = []

    try:
        contents = pagina.get("/Contents")

        if contents is None:
            return conteudos

        if isinstance(contents, pikepdf.Array):
            for item in contents:
                try:
                    conteudos.append(item.read_bytes())
                except Exception:
                    pass
        else:
            try:
                conteudos.append(contents.read_bytes())
            except Exception:
                pass

    except Exception:
        pass

    return conteudos


def analisar_xobjects(recursos, mapa_cores, resultado, visitados=None):
    if visitados is None:
        visitados = set()

    if recursos is None:
        return

    try:
        xobjects = recursos.get("/XObject", {})

        if not isinstance(xobjects, pikepdf.Dictionary):
            return

        for _, xobj in xobjects.items():
            obj_id = id(xobj)

            if obj_id in visitados:
                continue

            visitados.add(obj_id)

            subtype = str(xobj.get("/Subtype", ""))

            if subtype == "/Image":
                color_space = xobj.get("/ColorSpace")
                nome = nome_pdf_para_texto(color_space)

                if "DeviceCMYK" in nome:
                    resultado["CMYK"] = True
                    resultado["C"] = True
                    resultado["M"] = True
                    resultado["Y"] = True
                    resultado["K"] = True

                elif "DeviceRGB" in nome:
                    resultado["RGB"] = True

                elif "DeviceGray" in nome:
                    resultado["GRAY"] = True

            else:
                try:
                    analisar_stream_pdf(xobj.read_bytes(), mapa_cores, resultado)
                except Exception:
                    pass

                try:
                    sub_recursos = xobj.get("/Resources")
                    coletar_mapa_cores(sub_recursos, mapa_cores, resultado)
                    analisar_xobjects(sub_recursos, mapa_cores, resultado, visitados)
                except Exception:
                    pass

    except Exception:
        pass


def detectar_cores(pdf_bytes):
    resultado = {
        "CMYK": False,
        "RGB": False,
        "GRAY": False,
        "C": False,
        "M": False,
        "Y": False,
        "K": False,
        "SPOTS": set(),
    }

    with pikepdf.open(BytesIO(pdf_bytes)) as pdf:
        for pagina in pdf.pages:
            mapa_cores = {}

            recursos = pagina.get("/Resources")
            coletar_mapa_cores(recursos, mapa_cores, resultado)

            for conteudo in ler_bytes_conteudo_pagina(pagina):
                analisar_stream_pdf(conteudo, mapa_cores, resultado)

            analisar_xobjects(recursos, mapa_cores, resultado)

    spots_limpos = sorted(
        cor for cor in resultado["SPOTS"]
        if cor and cor not in IGNORE_SPOT_NAMES
    )

    return {
        "CMYK": resultado["CMYK"],
        "RGB": resultado["RGB"],
        "GRAY": resultado["GRAY"],
        "C": resultado["C"],
        "M": resultado["M"],
        "Y": resultado["Y"],
        "K": resultado["K"],
        "SPOTS": spots_limpos,
    }


def cor_escura(cor):
    if not cor:
        return True

    try:
        return all(c <= 0.25 for c in cor[:3])
    except Exception:
        return False


def detectar_marcas_de_corte(doc):
    total_linhas_suspeitas = 0

    for pagina in doc:
        desenhos = pagina.get_drawings()

        for desenho in desenhos:
            largura_linha = desenho.get("width", 0)

            if largura_linha is None or largura_linha > 1.2:
                continue

            if not cor_escura(desenho.get("color")):
                continue

            for item in desenho.get("items", []):
                if not item or item[0] != "l":
                    continue

                p1 = item[1]
                p2 = item[2]

                dx = abs(p2.x - p1.x)
                dy = abs(p2.y - p1.y)

                comprimento = max(dx, dy)
                comprimento_mm = pt_to_mm(comprimento)

                eh_horizontal = dy <= mm_to_pt(0.3) and dx > 0
                eh_vertical = dx <= mm_to_pt(0.3) and dy > 0

                if not (eh_horizontal or eh_vertical):
                    continue

                if 2 <= comprimento_mm <= 25:
                    total_linhas_suspeitas += 1

    return total_linhas_suspeitas >= 4


st.caption(
    "Envie um PDF para ler medidas, caixas técnicas, páginas, metadados e indícios de cor."
)

arquivo = st.file_uploader(
    "Enviar arquivo PDF",
    type=["pdf"],
    label_visibility="collapsed"
)

if arquivo:
    pdf_bytes = arquivo.read()

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        metadata = doc.metadata or {}
        boxes = analisar_boxes(pdf_bytes)
        cores = detectar_cores(pdf_bytes)
        marcas_corte = detectar_marcas_de_corte(doc)

        primeira = boxes[0]

        media_l, media_a = primeira["media"]
        trim_l, trim_a = primeira["trim"]

        col_preview, col_info = st.columns([0.65, 1.0], gap="medium")

        with col_preview:
            pagina = doc[0]
            pix = pagina.get_pixmap(matrix=fitz.Matrix(0.40, 0.40), alpha=False)

            st.image(pix.tobytes("png"))

            st.markdown(
                '<div class="preview-caption">Preview da primeira página</div>',
                unsafe_allow_html=True
            )

        with col_info:
            linha("Nome do arquivo", arquivo.name)
            linha("Peso", formatar_peso(len(pdf_bytes)))
            linha("Orientação", orientacao(media_l, media_a))
            linha("Criado em", metadata.get("creator") or "Não informado")
            linha("Data de criação", formatar_data_pdf(metadata.get("creationDate")))
            linha("Quantidade de páginas", str(len(doc)))

            separador()

            linha("Medida do PDF", formatar_mm(media_l, media_a))
            linha("Medida da marca de corte / Trim", formatar_mm(trim_l, trim_a))
            linha("Marcas de corte detectadas", "Sim" if marcas_corte else "Não")

            if not primeira["tem_trim"]:
                nota("TrimBox não definido. Usando MediaBox como referência.")

            separador()

            mostrar_separacoes(cores)

        if len(doc) > 1:
            separador()
            st.markdown("### Medidas por página")

            for item in boxes:
                st.caption(
                    f'Página {item["pagina"]} — '
                    f'PDF: {formatar_mm(*item["media"])} | '
                    f'Trim: {formatar_mm(*item["trim"])} | '
                    f'Bleed: {formatar_mm(*item["bleed"])}'
                )

    except Exception as erro:
        st.error("Não consegui ler este PDF com segurança.")
        st.code(str(erro))

else:
    st.markdown(
        """
<div style="margin-top:34px;padding:34px;border:1px dashed rgba(208,147,29,.4);border-radius:18px;text-align:center;background:rgba(208,147,29,.035);">

<div style="width:42px;height:52px;margin:0 auto 14px auto;border:3px solid #D0931D;border-radius:4px;position:relative;">
<div style="width:16px;height:3px;background:#D0931D;margin:14px auto 0 auto;"></div>
<div style="width:22px;height:3px;background:#D0931D;margin:8px auto 0 auto;"></div>
</div>

<div style="color:white;font-size:16px;font-weight:600;margin-bottom:6px;">
Envie um PDF para começar
</div>

<div style="color:rgba(255,255,255,.55);font-size:13px;">
A análise aparecerá aqui automaticamente.
</div>

</div>
        """,
        unsafe_allow_html=True
    )