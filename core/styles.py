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

        .stApp {{
            background-color: var(--m87-bg);
        }}

        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        section[data-testid="stSidebar"] {{
            min-width: 220px !important;
            width: 220px !important;
            max-width: 220px !important;
            background-color: var(--m87-bg) !important;
            border-right: 1px solid rgba(255,255,255,0.04) !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background-color: var(--m87-bg) !important;
            padding-top: 52px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] div[role="heading"],
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] p {{
            font-size: 9px !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.72) !important;
            line-height: 1.1 !important;
            margin-top: 10px !important;
            margin-bottom: 2px !important;
            padding-left: 12px !important;
        }}

        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] a p,
        section[data-testid="stSidebar"] a span {{
            font-size: 9px !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.72) !important;
            line-height: 1.1 !important;
            text-decoration: none !important;
        }}

        section[data-testid="stSidebar"] a {{
            border-radius: 10px !important;
            padding: 4px 12px 4px 20px !important;
            margin: 0 !important;
            min-height: auto !important;
            transition: all 0.18s ease !important;
        }}

        section[data-testid="stSidebar"] ul {{
            gap: 0px !important;
        }}

        section[data-testid="stSidebar"] li {{
            margin: 0 !important;
            padding: 0 !important;
        }}

        section[data-testid="stSidebar"] a:hover {{
            background-color: rgba(201,138,26,0.14) !important;
        }}

        section[data-testid="stSidebar"] a:hover p,
        section[data-testid="stSidebar"] a:hover span {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] a[aria-current="page"],
        section[data-testid="stSidebar"] a[data-active="true"] {{
            background-color: rgba(201,138,26,0.16) !important;
        }}

        section[data-testid="stSidebar"] a[aria-current="page"] p,
        section[data-testid="stSidebar"] a[aria-current="page"] span {{
            color: var(--m87-accent) !important;
        }}

        section[data-testid="stSidebar"] svg,
        section[data-testid="stSidebar"] img {{
            display: none !important;
        }}

        .stTextInput input,
        .stNumberInput input {{
            background-color: #222330 !important;
            border: 1px solid transparent !important;
            color: white !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: var(--m87-accent) !important;
            border: 1px solid var(--m87-accent) !important;
            color: white !important;
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
        }}

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
