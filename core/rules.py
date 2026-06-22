"""Regras e dados compartilhados do M87 Tools.

Tudo que pode ser usado por várias ferramentas fica aqui:
formatos padrão, tema, listas, unidades e presets.
"""

THEME = {
    "background": "#0E1117",
    "surface": "#111827",
    "surface_alt": "#1F2937",
    "border": "#374151",
    "text": "#FFFFFF",
    "muted": "#9CA3AF",
    "accent": "#C98A1A",
    "accent_hover": "#D99A27",
}

STANDARD_FORMATS = [
    {"nome": "A0", "largura": 841, "altura": 1189, "categoria": "ISO A"},
    {"nome": "A1", "largura": 594, "altura": 841, "categoria": "ISO A"},
    {"nome": "A2", "largura": 420, "altura": 594, "categoria": "ISO A"},
    {"nome": "A3", "largura": 297, "altura": 420, "categoria": "ISO A"},
    {"nome": "A4", "largura": 210, "altura": 297, "categoria": "ISO A"},
    {"nome": "A5", "largura": 148, "altura": 210, "categoria": "ISO A"},
    {"nome": "A6", "largura": 105, "altura": 148, "categoria": "ISO A"},
    {"nome": "A7", "largura": 74, "altura": 105, "categoria": "ISO A"},
    {"nome": "SRA3", "largura": 320, "altura": 450, "categoria": "SRA"},
    {"nome": "SRA4", "largura": 225, "altura": 320, "categoria": "SRA"},
    {"nome": "Cartão de visita EU", "largura": 85, "altura": 55, "categoria": "Comercial"},
    {"nome": "Cartão de visita BR", "largura": 90, "altura": 50, "categoria": "Comercial"},
    {"nome": "Envelope C6", "largura": 114, "altura": 162, "categoria": "Envelope"},
    {"nome": "Envelope DL", "largura": 110, "altura": 220, "categoria": "Envelope"},
    {"nome": "Envelope C5", "largura": 162, "altura": 229, "categoria": "Envelope"},
    {"nome": "Envelope C4", "largura": 229, "altura": 324, "categoria": "Envelope"},
]

PAPER_PRESETS = [
    {"nome": "A4", "largura": 210, "altura": 297},
    {"nome": "A3", "largura": 297, "altura": 420},
    {"nome": "SRA3", "largura": 320, "altura": 450},
    {"nome": "70 x 100 cm", "largura": 700, "altura": 1000},
    {"nome": "64 x 88 cm", "largura": 640, "altura": 880},
]

AREA_UNITS = {
    "mm": 1000,
    "cm": 100,
    "m": 1,
}

PREPRESS_CHECKLIST = [
    "Formato final correto",
    "Sangria aplicada",
    "Margem de segurança respeitada",
    "Fontes convertidas em curvas ou incorporadas",
    "Imagens com resolução suficiente",
    "Cores em CMYK quando necessário",
    "Pantones conferidos",
    "Overprint conferido",
    "Branco, verniz, faca ou hot stamping em layers separados",
    "Página única ou páginas na ordem correta",
    "Marcas de corte corretas",
    "Nome do arquivo com cliente, formato e versão",
]
