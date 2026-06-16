import math
import streamlit as st

from core.components import titulo_tool


st.markdown(
    """
    <style>
        .stCheckbox {
            margin-bottom: 2px;
        }

        .stCheckbox label {
            font-size: 0.92rem;
            line-height: 1.3;
            white-space: nowrap;
            color: #B8BDC7 !important;
        }

        .stCheckbox p {
            color: #B8BDC7 !important;
        }

        h2 {
            font-size: 1.08rem !important;
            margin-top: 26px !important;
            margin-bottom: 10px !important;
            color: #D7D7D7 !important;
        }

        div[data-testid="column"] {
            padding-right: 22px;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.08rem;
        }

        .postit-progresso {
            position: fixed;
            top: 90px;
            right: 28px;
            z-index: 9999;
            width: 220px;
            background: #d69413;
            color: white;
            padding: 14px 16px 12px 16px;
            border-radius: 14px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
            font-size: 0.9rem;
        }

        .postit-numero {
            font-weight: 700;
            margin-bottom: 8px;
        }

        .postit-barra {
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.35);
            border-radius: 999px;
            overflow: hidden;
        }

        .postit-fill {
            height: 100%;
            background: #e6ff00;
            border-radius: 999px;
        }

        .postit-mensagem {
            margin-top: 8px;
            font-size: 0.75rem;
            line-height: 1.2;
            opacity: 0.95;
        }

        .postit-rock {
            margin-top: 8px;
            font-size: 1.4rem;
            line-height: 1;
        }
        /* CHECKBOX MAIOR SEM AUMENTAR ALTURA TOTAL */
        div[data-testid="stCheckbox"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        div[data-testid="stCheckbox"] label {
            min-height: 24px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
        }
        
        div[data-testid="stCheckbox"] input {
            transform: scale(1.25);
            margin-right: 8px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


titulo_tool(
    "Check-list",
    "Conferência final antes de mandar o arquivo para produção."
)


CHECKLIST = {
    "ESTRUTURA DO ARQUIVO": [
        "Medida correta do material",
        "Sangria correta",
        "Marcas de corte",
    ],
    "FRENTE E VERSO": [
        "Frente correta",
        "Verso correto",
        "Orientação certa (cabeça com cabeça ou pé com pé)",
        "Conferir espelhamento",
    ],
    "CONTEÚDO": [
        "Textos revisados",
        "Textos 100% Preto",
        "Logos nítidos",
        "Transparências",
        "Imagens com qualidade",
        "Arquivos acabamento (Cortante, verniz)",
    ],
    "CORES": [
        "Arquivo em CMYK",
        "Preto correto (100% Preto)",
        "Overprint verificado",
        "Verificar Pantones",
        "Cortante sobreposto?",
    ],
    "ARQUIVO FINAL": [
        "PDF exportado com sangria",
        "PDF com espaço de 5mm",
        "Salvar PDF e AI",
        "Indicar versão do arquivo",
    ],
    "REVISÃO FINAL": [
        "Conferido visualmente",
        "Impressão de prova de chapa",
        "Impressão de modelo (Quantidade/planos/papel/data)",
        "Assinar",
        "Aprovação do cliente",
    ],
}


def limpar_checklist():
    for chave in list(st.session_state.keys()):
        if chave.startswith("check_"):
            st.session_state[chave] = False


total = sum(len(itens) for itens in CHECKLIST.values())

feito = sum(
    1
    for chave, valor in st.session_state.items()
    if chave.startswith("check_") and valor is True
)

percentual = feito / total if total else 0
largura_barra = percentual * 100


if feito == total:
    mensagem_status = "Tudo pronto!"
    rock_status = "🤘🤘🤘"
elif feito >= total * 0.75:
    mensagem_status = "Quase lá. Falta pouco."
    rock_status = ""
else:
    mensagem_status = "Ainda faltam pontos importantes."
    rock_status = ""


st.markdown(
    f"""
    <div class="postit-progresso">
        <div class="postit-numero">Conferido: {feito}/{total}</div>
        <div class="postit-barra">
            <div class="postit-fill" style="width: {largura_barra}%;"></div>
        </div>
        <div class="postit-mensagem">{mensagem_status}</div>
        <div class="postit-rock">{rock_status}</div>
    </div>
    """,
    unsafe_allow_html=True
)


for categoria, itens in CHECKLIST.items():
    st.markdown(f"## {categoria}")

    meio = math.ceil(len(itens) / 2)
    itens_esquerda = itens[:meio]
    itens_direita = itens[meio:]

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        for item in itens_esquerda:
            st.checkbox(
                item,
                key=f"check_{categoria}_{item}"
            )

    with col2:
        for item in itens_direita:
            st.checkbox(
                item,
                key=f"check_{categoria}_{item}"
            )


st.markdown("---")

st.button(
    "Limpar checklist",
    on_click=limpar_checklist,
    use_container_width=True
)
