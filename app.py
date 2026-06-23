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
        st.Page("tools/novo_orcamento.py", title="NOVO ORÇAMENTO"),
        st.Page("tools/orcamento_aprovado.py", title="ORÇAMENTO APROVADO"),
        st.Page("tools/cadastro_clientes.py", title="CADASTRO DE CLIENTES"),
    ],
     
        "CALCULADORAS": [
        st.Page("tools/calculadora_formatos.py", title="FORMATOS (MONTAGENS)", default=True),
        st.Page("tools/peso_papel.py", title="PESO DE PAPEL"),
        st.Page("tools/area_m2.py", title="ÁREA EM M²"),
        st.Page("tools/preco_papel.py", title="PREÇO DO PAPEL"),
    ],

        "CHECKLISTS": [
        st.Page("tools/checklist_pre_impressao.py", title="PRÉ-IMPRESSÃO"),
        st.Page("tools/checklist_saida_producao.py", title="SAÍDA PARA PRODUÇÃO"),
        st.Page("tools/checklist_pfi.py", title="CORTE / VINCO / PFI"),
    ],

    "FERRAMENTAS": [
        st.Page("tools/biblioteca_formatos.py", title="FORMATOS"),
        st.Page("tools/info_pdf.py", title="INFO PDF"),
    ],
}

navegacao = st.navigation(paginas, position="sidebar")
navegacao.run()