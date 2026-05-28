# M87 TOOLS

Ferramentas para gráfica, pré-impressão e produção gráfica desenvolvidas em Python + Streamlit.

Projeto criado para transformar cálculos repetitivos, conferências técnicas e pequenos processos do dia a dia em ferramentas rápidas, visuais e práticas.

---

## Objetivo do projeto

O M87 Tools nasceu da ideia de criar uma central de utilidades para produção gráfica.

A proposta é simples:

> abrir → calcular → conferir → produzir

Sem planilhas gigantes.
Sem fórmulas espalhadas.
Sem ficar refazendo cálculo no papel ou na calculadora do celular.

Tudo pensado para funcionar de forma rápida, limpa e visual.

---

# Tecnologias usadas

* Python
* Streamlit
* Matplotlib

---

# Estrutura atual do projeto

```bash
m87-tools/
│
├── app.py
│
└── tools/
    ├── formatos.py
    ├── peso_papel.py
    ├── area_m2.py
    ├── checklist_pre_impressao.py
    └── biblioteca_formatos.py
```

---

# Ferramentas atuais

## Calculadora de Formatos

Calcula automaticamente:

* peças por folha
* melhor aproveitamento
* rotação da peça
* quantidade de planos
* excedente
* margem de segurança
* espaço entre peças

Também gera um desenho técnico da montagem.

---

## Calculadora de Peso de Papel

Calcula o peso total baseado em:

* largura
* altura
* gramatura
* quantidade

Ideal para:

* orçamentos
* envio
* logística
* conferência de produção

---

## Calculadora de Área em m²

Calcula áreas para:

* papel
* adesivo
* lona
* vinil
* placas
* banners

Permite trabalhar em:

* mm
* cm
* metros

---

## Checklist Pré-Impressão

Checklist rápido para conferência de arquivos antes da produção.

Inclui verificações como:

* sangria
* CMYK
* fontes em curvas
* overprint
* resolução
* imagens linkadas
* marcas de corte

---

## Biblioteca de Formatos

Consulta rápida de formatos padrão:

* A4
* A3
* SRA3
* cartões
* flyers
* formatos gráficos comuns

---

# Navegação

O projeto utiliza uma navegação lateral fixa.

A calculadora principal abre automaticamente ao acessar o site, enquanto as demais ferramentas ficam disponíveis no menu lateral.

---

# Filosofia do projeto

O foco não é criar um sistema corporativo pesado.

A ideia é construir ferramentas:

* rápidas
* diretas
* bonitas
* úteis no mundo real

Ferramentas feitas por quem trabalha diariamente com impressão, fechamento e produção gráfica.

---

# Próximas ferramentas planejadas

* calculadora de custo por peça
* cálculo de lombada
* cálculo de DPI real
* impositor automático
* simulador de desperdício
* ficha técnica automática
* ordem de produção
* calculadora de sangria
* comparador de formatos

---

# Rodando localmente

Clone o projeto:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd m87-tools
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
streamlit run app.py
```

---

# Deploy

O projeto está preparado para deploy no:

* Streamlit Cloud

Basta conectar o repositório GitHub.

---

# Autor

M87 • Tools

Desenvolvido para gráfica, pré-impressão e produção real.
