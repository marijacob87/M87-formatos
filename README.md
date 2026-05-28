# M87 Tools

Ferramentas para gráfica, pré-impressão e produção gráfica feitas em Python + Streamlit.

## Estrutura atual

```text
m87_tools/
├── app.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── components.py
│   ├── rules.py
│   ├── styles.py
│   └── utils.py
└── tools/
    ├── formatos.py
    ├── peso_papel.py
    ├── area_m2.py
    ├── checklist_pre_impressao.py
    └── biblioteca_formatos.py
```

## Organização

- `app.py`: entrada principal do Streamlit e navegação lateral.
- `core/styles.py`: CSS global do app, incluindo sidebar, botões e cards.
- `core/components.py`: componentes visuais reutilizáveis, como título e cards.
- `core/rules.py`: regras, formatos, listas e dados usados por várias ferramentas.
- `core/utils.py`: funções úteis compartilhadas.
- `tools/`: páginas/ferramentas individuais.

## Rodar localmente

```bash
streamlit run app.py
```

## Ferramentas atuais

- Calculadora de Formatos
- Calculadora de Peso de Papel
- Calculadora de Área em m²
- Checklist Pré-Impressão
- Biblioteca de Formatos Padrão
