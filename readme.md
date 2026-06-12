# M87 TOOLS

Ferramentas para pré-impressão, produção gráfica e orçamentos, desenvolvidas em Python + Streamlit para otimizar tarefas do dia a dia em gráfica.

🔗 Aplicação online:

https://m87-calc.streamlit.app

---

# Objetivo

O M87 TOOLS nasceu para reduzir cálculos manuais, diminuir erros de produção e concentrar em um único lugar ferramentas que normalmente ficam espalhadas entre planilhas, calculadoras, blocos de notas e consultas rápidas.

A filosofia do projeto é simples:

**Conferir → Calcular → Produzir**

---

# Funcionalidades

## CALCULADORAS

### FORMATOS (MONTAGENS)

Calcula automaticamente:

- Quantidade de peças por folha
- Melhor aproveitamento
- Segunda melhor opção de montagem
- Produção final
- Excedente de produção
- Aproveitamento da folha
- Quantidade de folhas necessárias
- Margens
- Espaçamentos
- Rotação automática para melhor encaixe

Status: ✅ Funcional

---

### PESO DE PAPEL

Calcula:

- Área unitária
- Peso unitário
- Peso total
- Quantidade de folhas por quilo

Com base em:

- Largura
- Altura
- Gramatura
- Quantidade

Status: ✅ Funcional

---

### ÁREA EM M²

Calcula:

- Área unitária
- Área total

Ideal para:

- Vinil
- Lona
- PVC
- Acrílico
- Papel
- Adesivos
- Materiais vendidos por área

Status: ✅ Funcional

---

### PREÇO DO PAPEL

Calculadora para determinar:

- Quantidade de folhas por quilo
- Custo por folha
- Custo por material

Status: 🚧 Em desenvolvimento

---

# ORÇAMENTOS

### NOVO ORÇAMENTO

Ferramenta para criação e organização de pedidos de orçamento gráfico.

Status: 🚧 Em desenvolvimento

---

### ORÇAMENTO APROVADO

Controle de orçamentos aprovados e produção.

Status: 🚧 Em desenvolvimento

---

### CADASTRO DE CLIENTES

Base de clientes para utilização integrada aos orçamentos.

Status: 🚧 Em desenvolvimento

---

# CHECKLISTS

### PRÉ-IMPRESSÃO

Checklist visual para conferência final dos arquivos antes do envio para produção.

Inclui validações como:

- Sangria
- Margens
- Fontes
- Imagens
- Escala
- Orientação
- Quantidade
- Acabamentos

Status: ✅ Funcional

---

### SAÍDA PARA PRODUÇÃO

Checklist de conferência antes da liberação para impressão.

Status: 🚧 Em desenvolvimento

---

### CORTE / VINCO / PFI

Checklist específico para processos de acabamento.

Status: 🚧 Em desenvolvimento

---

# FERRAMENTAS

### BIBLIOTECA DE FORMATOS

Biblioteca com medidas utilizadas frequentemente na produção gráfica.

Status: 🚧 Em desenvolvimento

---

### ACABAMENTOS

Consulta rápida de acabamentos gráficos.

Status: 🚧 Em desenvolvimento

---

# Estrutura do Projeto

```text
M87-formatos/
│
├── app.py
│
├── core/
│   ├── __init__.py
│   ├── components.py
│   ├── rules.py
│   ├── styles.py
│   └── utils.py
│
├── tools/
│   ├── calculadora_formatos.py
│   ├── peso_papel.py
│   ├── area_m2.py
│   ├── preco_papel.py
│   ├── novo_orcamento.py
│   ├── orcamento_aprovado.py
│   ├── cadastro_clientes.py
│   ├── checklist_pre_impressao.py
│   ├── checklist_saida_producao.py
│   ├── checklist_pfi.py
│   ├── biblioteca_formatos.py
│   └── acabamentos.py
│
├── requirements.txt
└── README.md
```

---

# Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Matplotlib

---

# Público-Alvo

Este projeto foi criado principalmente para:

- Arte-finalistas
- Operadores de pré-impressão
- Designers gráficos
- Gráficas rápidas
- Comunicação visual
- Produção gráfica

---

# Roadmap

Planejamento das próximas funcionalidades:

- Histórico de cálculos
- Banco de materiais
- Banco de papéis
- Cadastro de fornecedores
- Sistema de orçamento completo
- Impressão de fichas de produção
- Biblioteca técnica de acabamentos
- Integração com Illustrator
- Integração com o projeto M87 IMPOSITOR

---

# Autor

**Mariane Jacob**

Projeto desenvolvido para uso profissional em pré-impressão e produção gráfica.

**M87 TOOLS**
