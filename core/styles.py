"""CSS global do M87 Tools."""


def carregar_css():
    amarelo = "#D0931D"
    amarelo_hover = "#B8821A"
    fundo = "#0E1117"
    

    return f"""
    <style>
        .menu-ok {{
            color: #35e66b !important;
            font-size: 7px !important;
            margin-right: 7px !important;
            text-shadow: 0 0 8px rgba(53,230,107,0.75);

        }}

            .stApp {{
            background-color: {fundo};

        }}

        .stApp {{
            background-color: {fundo};
        }}

        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            min-width: 220px !important;
            width: 220px !important;
            max-width: 220px !important;
            background-color: {fundo} !important;
            border-right: 1px solid rgba(255,255,255,0.04) !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background-color: {fundo} !important;
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
            font-size: 10.5px !important;
            font-weight: 800 !important;
            letter-spacing: 1.8px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.76) !important;
            line-height: 1.25 !important;
            text-decoration: none !important;
        }}

        section[data-testid="stSidebar"] a {{
            border-radius: 10px !important;
            padding: 5px 12px 5px 20px !important;
            margin-bottom: 3px !important;
            transition: all 0.18s ease !important;
        }}

        section[data-testid="stSidebar"] a:hover {{
            background-color: rgba(201,138,26,0.14) !important;
        }}

        section[data-testid="stSidebar"] a[aria-current="page"],
        section[data-testid="stSidebar"] a[data-active="true"] {{
            background-color: rgba(201,138,26,0.16) !important;
            color: {amarelo} !important;
        }}

        section[data-testid="stSidebar"] svg,
        section[data-testid="stSidebar"] img {{
            display: none !important;
        }}

        .m87-brand {{
            text-align: center;
            color: {amarelo};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 0px;
            margin-bottom: 12px;
        }}

        /* Botões gerais */
        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: {amarelo} !important;
            border: 1px solid {amarelo} !important;
            color: white !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {{
            background-color: {amarelo_hover} !important;
            border-color: {amarelo_hover} !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab"],
        .stTabs [data-baseweb="tab"] p {{
            color: {amarelo} !important;
            font-weight: 700 !important;
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: {amarelo} !important;
        }}

        /* Inputs em foco */
        input:focus,
        input:focus-visible,
        textarea:focus,
        textarea:focus-visible,
        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus {{
            border-color: {amarelo} !important;
            box-shadow: 0 0 0 1px {amarelo} !important;
            outline: none !important;
        }}

        div:has(> input:focus),
        div:has(> input:focus-visible) {{
            border-color: {amarelo} !important;
            box-shadow: 0 0 0 1px {amarelo} !important;
        }}

        /* Number input +/- */
        [data-testid="stNumberInput"] button {{
            background-color: {amarelo} !important;
            border-color: {amarelo} !important;
            color: white !important;
        }}

        [data-testid="stNumberInput"] button:hover {{
            background-color: {amarelo_hover} !important;
            border-color: {amarelo_hover} !important;
            color: white !important;
        }}

        /* Checkbox */
        [data-testid="stCheckbox"] svg,
        [data-baseweb="checkbox"] svg {{
            color: {amarelo} !important;
            fill: {amarelo} !important;
        }}

        [data-baseweb="checkbox"] div {{
            border-color: {amarelo} !important;
        }}

        /* Radio */
        div[role="radiogroup"] label span:first-child {{
            border-color: {amarelo} !important;
        }}

        div[role="radiogroup"] label span:first-child > span {{
            background-color: {amarelo} !important;
        }}

        /* Segmented control */
        button[data-testid="stBaseButton-segmented_controlActive"] {{
            background-color: {amarelo} !important;
            border-color: {amarelo} !important;
            color: white !important;
        }}

        button[data-testid="stBaseButton-segmented_controlActive"] p {{
            color: white !important;
        }}

        button[data-testid="stBaseButton-segmented_control"] {{
            border-color: rgba(208,147,29,0.55) !important;
            color: white !important;
        }}

        button[data-testid="stBaseButton-segmented_control"] p {{
            color: white !important;
        }}

        .stMarkdown li::marker {{
            color: {amarelo} !important;
        }}
        
    </style>
    """