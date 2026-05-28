"""CSS global do M87 Tools."""
from .rules import THEME


def carregar_css():
    t = THEME
    return f"""
    <style>
        :root {{
            --m87-bg: {t['background']};
            --m87-surface: {t['surface']};
            --m87-surface-alt: {t['surface_alt']};
            --m87-border: {t['border']};
            --m87-text: {t['text']};
            --m87-muted: {t['muted']};
            --m87-accent: {t['accent']};
            --m87-accent-hover: {t['accent_hover']};
        }}

        /* Esconde o botão de recolher sidebar */
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        /* Sidebar fixa, mais fina e com a mesma cor do fundo */
        section[data-testid="stSidebar"] {{
            min-width: 235px !important;
            width: 235px !important;
            max-width: 235px !important;
            background-color: var(--m87-bg) !important;
            border-right: 1px solid rgba(255,255,255,0.04) !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background-color: var(--m87-bg) !important;
            padding-top: 52px !important;
            padding-left: 12px !important;
            padding-right: 12px !important;
        }}

        /* Links da navegação */
        section[data-testid="stSidebar"] a {{
            font-size: 10px !important;
            font-weight: 800 !important;
            letter-spacing: 1.35px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.66) !important;
            border-radius: 8px !important;
            padding: 7px 10px !important;
            margin-bottom: 5px !important;
            line-height: 1.15 !important;
        }}

        section[data-testid="stSidebar"] a:hover {{
            color: #FFFFFF !important;
            background-color: rgba(201,138,26,0.14) !important;
        }}

        section[data-testid="stSidebar"] a[aria-current="page"],
        section[data-testid="stSidebar"] a[data-active="true"] {{
            color: var(--m87-accent) !important;
            background-color: rgba(201,138,26,0.15) !important;
        }}

        /* Remove/neutraliza espaços de ícones da navegação, se o Streamlit gerar algum */
        section[data-testid="stSidebar"] svg,
        section[data-testid="stSidebar"] img {{
            display: none !important;
        }}

        /* Botões globais */
        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: var(--m87-accent) !important;
            border: 1px solid var(--m87-accent) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
            min-height: 52px !important;
            font-size: 15px !important;
            box-shadow: none !important;
        }}

        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {{
            background-color: var(--m87-accent-hover) !important;
            border-color: var(--m87-accent-hover) !important;
            color: #FFFFFF !important;
        }}

        div[data-testid="stButton"] > button:focus,
        div[data-testid="stFormSubmitButton"] > button:focus {{
            box-shadow: 0 0 0 2px rgba(201,138,26,0.28) !important;
        }}

        /* Cards M87 */
        .card-m87 {{
            background: linear-gradient(135deg, var(--m87-surface), var(--m87-surface-alt));
            border: 1px solid var(--m87-border);
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 10px 24px rgba(0,0,0,0.18);
            min-height: 65px;
            margin-bottom: 0px;
        }}

        .card-label {{
            font-size: 9px;
            color: var(--m87-muted);
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 700;
            margin-bottom: 14px;
        }}

        .card-value {{
            font-size: 30px;
            color: var(--m87-text);
            font-weight: 800;
            line-height: 1;
        }}

        .card-extra {{
            font-size: 12px;
            color: #D1D5DB;
            margin-top: 7px;
        }}

        .m87-brand {{
            text-align: center;
            color: var(--m87-accent);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 0px;
            margin-bottom: 12px;
        }}
    </style>
    """
