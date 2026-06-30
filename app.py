import streamlit as st

from core.components import aplicar_estilo_global

st.set_page_config(
    page_title="M87 Tools",
    layout="centered",
    initial_sidebar_state="expanded"
)

aplicar_estilo_global()

paginas = {
    "ORÇAMENTOS": [
        st.Page("tools/1_orcamentos/novo_orcamento.py", title="NOVO ORÇAMENTO"),
        st.Page("tools/1_orcamentos/orcamento_aprovado.py", title="ORÇAMENTO APROVADO"),
        st.Page("tools/1_orcamentos/cadastro_clientes.py", title="CADASTRO DE CLIENTES"),
    ],

    "CALCULADORAS": [
        st.Page("tools/2_calculadoras/calculadora_formatos.py", title="● FORMATOS (MONTAGENS)", default=True),
        st.Page("tools/2_calculadoras/peso_papel.py", title="● PESO DE PAPEL"),
        st.Page("tools/2_calculadoras/area_m2.py", title="● ÁREA EM M²"),
        st.Page("tools/2_calculadoras/preco_papel.py", title="● PREÇO DO PAPEL"),
    ],

    "CHECKLISTS": [
        st.Page("tools/3_checklists/checklist_pre_impressao.py", title="● PRÉ-IMPRESSÃO"),
        st.Page("tools/3_checklists/checklist_saida_producao.py", title=" SAÍDA PARA PRODUÇÃO"),
        st.Page("tools/3_checklists/checklist_pfi.py", title=" CORTE / VINCO / PFI"),
    ],

    "FERRAMENTAS": [
        st.Page("tools/4_ferramentas/biblioteca_formatos.py", title="● FORMATOS"),
        st.Page("tools/4_ferramentas/info_pdf.py", title="● INFO PDF"),
        st.Page("tools/4_ferramentas/barcodegenerator.py", title="● EAN13 e QRCODE"),
    ],
}

navegacao = st.navigation(
    paginas,
    position="sidebar"
)

navegacao.run()