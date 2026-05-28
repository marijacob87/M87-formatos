import streamlit as st


st.markdown("""
<div style="text-align:center;color:#C98A1A;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
BY @M87 • TOOLS
</div>
""", unsafe_allow_html=True)

st.subheader("Checklist Pré-impressão")
st.caption("Uma lista rápida para não mandar um PDF possuído para produção.")

itens = [
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

marcados = []

for item in itens:
    if st.checkbox(item):
        marcados.append(item)

total = len(itens)
feito = len(marcados)
percentual = feito / total if total else 0

st.progress(percentual)
st.write(f"Conferido: **{feito}/{total}**")

if feito == total:
    st.success("Arquivo pronto para produção.")
elif feito >= total * 0.75:
    st.info("Quase lá. Ainda tem alguns fantasminhas no PDF.")
else:
    st.warning("Ainda faltam pontos importantes antes de enviar.")
