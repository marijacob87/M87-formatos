import streamlit as st
import fitz  # PyMuPDF
import pikepdf
from datetime import datetime
from io import BytesIO


MM_PER_POINT = 25.4 / 72


st.set_page_config(
    page_title="M87 • INFO PDF",
    page_icon="📄",
    layout="wide"
)


st.markdown("""
<style>
    .stApp {
        background-color: #1f2523;
        color: #f2f2f2;
    }

    h1, h2, h3, p, label, span, div {
        color: #f2f2f2;
    }

    .info-card {
        background: #252c29;
        border: 1px solid #3a423f;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .label {
        font-size: 0.85rem;
        color: #b7beb9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
    }

    .value {
        font-size: 1.35rem;
        color: #f2f2f2;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .warning {
        background: #4a3b1f;
        color: #ffd27a;
        padding: 10px 14px;
        border-radius: 10px;
        margin-top: 8px;
        font-size: 0.95rem;
    }

    .ok {
        background: #253f31;
        color: #91e6b3;
        padding: 10px 14px;
        border-radius: 10px;
        margin-top: 8px;
        font-size: 0.95rem;
    }

    .small {
        color: #b7beb9;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def pt_to_mm(value):
    return round(float(value) * MM_PER_POINT, 2)


def box_to_mm(box):
    width_pt = float(box[2]) - float(box[0])
    height_pt = float(box[3]) - float(box[1])
    return pt_to_mm(width_pt), pt_to_mm(height_pt)


def format_mm(width, height):
    return f"{width:.1f} mm x {height:.1f} mm"


def get_orientation(width, height):
    if abs(width - height) < 0.5:
        return "Quadrado"
    if width > height:
        return "Paisagem"
    return "Retrato"


def format_pdf_date(raw_date):
    if not raw_date:
        return "Não informado"

    try:
        clean = raw_date.replace("D:", "")
        dt = datetime.strptime(clean[:14], "%Y%m%d%H%M%S")
        return dt.strftime("%d/%m/%Y às %H:%M")
    except Exception:
        return raw_date


def get_file_size(size_bytes):
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


def analyze_boxes(pdf_bytes):
    result = []

    with pikepdf.open(BytesIO(pdf_bytes)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            media = page.get("/MediaBox")
            trim = page.get("/TrimBox")
            bleed = page.get("/BleedBox")
            crop = page.get("/CropBox")

            media_mm = box_to_mm(media)
            trim_mm = box_to_mm(trim) if trim else media_mm
            bleed_mm = box_to_mm(bleed) if bleed else media_mm
            crop_mm = box_to_mm(crop) if crop else media_mm

            result.append({
                "page": index,
                "media": media_mm,
                "trim": trim_mm,
                "bleed": bleed_mm,
                "crop": crop_mm,
                "has_trim": trim is not None,
                "has_bleed": bleed is not None,
                "has_crop": crop is not None
            })

    return result


def detect_colors(pdf_bytes):
    text = pdf_bytes.decode("latin-1", errors="ignore")

    detected = {
        "CMYK": False,
        "RGB": False,
        "Gray": False,
        "Spot": False,
        "Pantones": []
    }

    cmyk_signals = ["/DeviceCMYK", "/ICCBased", "CMYK"]
    rgb_signals = ["/DeviceRGB", "RGB"]
    gray_signals = ["/DeviceGray", "Gray"]
    spot_signals = ["/Separation", "/DeviceN", "/Spot"]

    detected["CMYK"] = any(signal in text for signal in cmyk_signals)
    detected["RGB"] = any(signal in text for signal in rgb_signals)
    detected["Gray"] = any(signal in text for signal in gray_signals)
    detected["Spot"] = any(signal in text for signal in spot_signals)

    possible_pantones = []
    for part in text.split("/"):
        if "PANTONE" in part.upper():
            name = part.split()[0]
            name = name.replace("#20", " ")
            possible_pantones.append(name)

    detected["Pantones"] = sorted(set(possible_pantones))

    return detected


def show_field(label, value):
    st.markdown(f"""
    <div class="label">{label}</div>
    <div class="value">{value}</div>
    """, unsafe_allow_html=True)


st.title("📄 M87 • INFO PDF")

st.markdown(
    "Sobe um PDF e a ferramenta lê medidas, caixas técnicas, metadados e indícios de cor. "
    "Para pré-impressão, ela mostra também quando alguma informação não está realmente definida no arquivo."
)

uploaded_file = st.file_uploader("Enviar PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        metadata = doc.metadata or {}
        boxes = analyze_boxes(pdf_bytes)
        colors = detect_colors(pdf_bytes)

        first_page = boxes[0]
        media_w, media_h = first_page["media"]
        trim_w, trim_h = first_page["trim"]
        bleed_w, bleed_h = first_page["bleed"]

        col_preview, col_info = st.columns([1, 2])

        with col_preview:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)

            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.25, 0.25), alpha=False)
            st.image(pix.tobytes("png"), caption="Preview da primeira página")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)

            show_field("Arquivo", uploaded_file.name)
            show_field("Peso", get_file_size(len(pdf_bytes)))
            show_field("Medida do PDF", format_mm(media_w, media_h))
            show_field("Orientação", get_orientation(media_w, media_h))
            show_field("Medida da marca de corte / Trim", format_mm(trim_w, trim_h))

            if first_page["has_trim"]:
                st.markdown('<div class="ok">TrimBox definido no PDF.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning">⚠️ TrimBox não definido. Usando MediaBox como referência.</div>', unsafe_allow_html=True)

            show_field("Bleed", format_mm(bleed_w, bleed_h))

            if first_page["has_bleed"]:
                st.markdown('<div class="ok">BleedBox definido no PDF.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning">⚠️ BleedBox não definido. Usando MediaBox como referência.</div>', unsafe_allow_html=True)

            show_field("Páginas", str(len(doc)))
            show_field("Data de criação", format_pdf_date(metadata.get("creationDate")))
            show_field("Criado em", metadata.get("creator") or "Não informado")
            show_field("Produtor PDF", metadata.get("producer") or "Não informado")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Cores detectadas")

        color_list = []

        if colors["CMYK"]:
            color_list.append("CMYK")
        if colors["RGB"]:
            color_list.append("RGB")
        if colors["Gray"]:
            color_list.append("Gray / Escala de cinza")
        if colors["Spot"]:
            color_list.append("Spot / Cor especial")

        if color_list:
            show_field("Espaços de cor encontrados", ", ".join(color_list))
        else:
            show_field("Espaços de cor encontrados", "Nenhum sinal claro detectado")

        if colors["Pantones"]:
            show_field("Pantones / Cores especiais", ", ".join(colors["Pantones"]))
        else:
            show_field("Pantones / Cores especiais", "Nenhuma detectada")

        st.markdown("""
        <div class="warning">
        ⚠️ A leitura de cores é uma análise por sinais internos do PDF. 
        Para produção crítica, conferir no Acrobat, PitStop ou Callas.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if len(doc) > 1:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.subheader("Medidas por página")

            for item in boxes:
                st.markdown(f"""
                <div class="small">
                Página {item["page"]} — 
                PDF: {format_mm(*item["media"])} | 
                Trim: {format_mm(*item["trim"])} | 
                Bleed: {format_mm(*item["bleed"])}
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as error:
        st.error("Não consegui ler este PDF com segurança.")
        st.code(str(error))
else:
    st.info("Envia um PDF para começar a análise.")