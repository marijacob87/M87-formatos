"""CSS global do M87 Tools."""


def carregar_css():
    return """
    
    <style>
        .stApp {
            background-color: #0E1117;
        }

        
        /* Segmented control */
        [data-testid="stSegmentedControl"] button {
            color: #FFFFFF !important;
            border-color: #D0931D !important;
        }

        [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
            background-color: #D0931D !important;
            color: #FFFFFF !important;
            border-color: #D0931D !important;
        }

        [data-testid="stSegmentedControl"] button p {
            color: inherit !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }

        section[data-testid="stSidebar"] {
            min-width: 220px !important;
            width: 220px !important;
            max-width: 220px !important;
            background-color: #0E1117 !important;
            border-right: 1px solid rgba(255,255,255,0.04) !important;
        }

        section[data-testid="stSidebar"] > div {
            background-color: #0E1117 !important;
            padding-top: 52px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] div[role="heading"],
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] p {
            font-size: 9px !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.72) !important;
            line-height: 1.1 !important;
            margin-top: 10px !important;
            margin-bottom: 2px !important;
            padding-left: 12px !important;
        }

        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] a p,
        section[data-testid="stSidebar"] a span {
            font-size: 9px !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.72) !important;
            line-height: 1.1 !important;
            text-decoration: none !important;
        }

        section[data-testid="stSidebar"] a {
            border-radius: 10px !important;
            padding: 4px 12px 4px 20px !important;
            margin-bottom: 1px !important;
            transition: all 0.18s ease !important;
        }

        section[data-testid="stSidebar"] a:hover {
            background-color: rgba(201,138,26,0.14) !important;
        }

        section[data-testid="stSidebar"] a[aria-current="page"],
        section[data-testid="stSidebar"] a[data-active="true"] {
            background-color: rgba(201,138,26,0.16) !important;
            color: #d99a1b !important;
        }

        section[data-testid="stSidebar"] svg,
        section[data-testid="stSidebar"] img {
            display: none !important;
        }

        .m87-brand {
            text-align: center;
            color: #d99a1b;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 0px;
            margin-bottom: 12px;
        }

        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #D0931D !important;
            border: 1px solid #D0931D !important;
            color: white !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
        }

        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #B8821A !important;
            border-color: #B8821A !important;
        }

        .stTabs [data-baseweb="tab"] {
            color: #D0931D !important;
            font-weight: 700 !important;
        }

        .stTabs [data-baseweb="tab"] p {
            color: #D0931D !important;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #D0931D !important;
        }

        div[role="radiogroup"] label span:first-child {
            border-color: #D0931D !important;
        }

        div[role="radiogroup"] label span:first-child > span {
            background-color: #D0931D !important;
        }

        [data-testid="stNumberInput"] button {
            background-color: #D0931D !important;
            border-color: #D0931D !important;
            color: white !important;
        }

        [data-testid="stNumberInput"] button:hover {
            background-color: #B8821A !important;
            border-color: #B8821A !important;
            color: white !important;
        }

        .stMarkdown li::marker {
            color: #D0931D !important;
        }

    </style>
    """