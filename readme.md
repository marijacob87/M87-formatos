# M87 Tools

Ferramentas para gráfica, pré-impressão e produção gráfica desenvolvidas em Python e Streamlit.

O projeto reúne utilitários rápidos para cálculos comuns, conferências técnicas e apoio em decisões de produção.

---

## Objetivo

Simplificar o fluxo de trabalho de quem atua em impressão e pré-impressão:

* abrir → calcular → conferir → produzir
* reduzir retrabalho e erros manuais
* evitar planilhas complexas e cálculos fora do fluxo
* oferecer resultados visuais e fáceis de usar

---

## Tecnologias

* Python
* Streamlit
* Matplotlib
* Pandas

---

## Estrutura do projeto

```bash
M87-formatos/
├── app.py
├── components.py
├── requirements.txt
├── rules.py
├── styles.py
├── utils.py
├── core/
│   ├── __init__.py
│   ├── components.py
│   ├── rules.py
│   ├── styles.py
│   └── utils.py
└── tools/
    ├── area_m2.py
    ├── biblioteca_formatos.py
    ├── calculadora_formatos.py
    ├── checklist_pre_impressao.py
    ├── novo_orcamento.py
    ├── peso_papel.py
    ├── preco_papel.py
    └── formatos.py
```

---

## Ferramentas disponíveis

### Calculadoras

* `FORMATOS (MONTAGENS)` — cálculo de aproveitamento, peças por folha, rotação, planos, excesso e espaço entre peças
* `PESO DE PAPEL` — peso final considerando dimensões, gramatura e quantidade
* `ÁREA EM M²` — conversão e cálculo de área para papéis, lonas, vinis e outros materiais
* `PREÇO DO PAPEL` — cálculo de custo de material com base em preço por kg ou m²

### Ferramentas adicionais

* `NOVO ORÇAMENTO` — base para criação de propostas de produção
* `CHECK LIST PRÉ IMPRESSÃO` — conferência de itens importantes antes de enviar para produção
* `BIBLIOTECA DE FORMATOS` — consulta de formatos padrão e medidas comuns

---

## Navegação

O aplicativo usa navegação lateral padrão do Streamlit. As calculadoras aparecem na seção de "CALCULADORAS" e as demais ferramentas na seção "FERRAMENTAS".

---

## Como executar

1. Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

2. Acesse a pasta do projeto:

```bash
cd M87-formatos
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
streamlit run app.py
```

---

## Observações

* O projeto é ideal para profissionais de produção gráfica que precisam de cálculos rápidos sem planilhas complexas.
* O design é focado em usabilidade e velocidade.
* A base permite evoluir com novas ferramentas de cálculo e conferência.


O projeto está preparado para deploy no:

* Streamlit Cloud

Basta conectar o repositório GitHub.

---

# Autor

M87 • Tools

Desenvolvido para gráfica, pré-impressão e produção real.
