"""Funções utilitárias compartilhadas."""


def converter_numero(valor):
    """Converte texto em número, aceitando vírgula ou ponto.

    Retorna None quando o campo está vazio ou inválido.
    """
    if valor is None:
        return None

    valor = str(valor).strip()
    if valor == "":
        return None

    try:
        return float(valor.replace(",", "."))
    except ValueError:
        return None


def numero_ok(valor, permite_zero=False):
    if valor is None:
        return False
    return valor >= 0 if permite_zero else valor > 0


def formatar_numero(valor, casas=2):
    if valor is None:
        return "-"
    texto = f"{valor:.{casas}f}"
    return texto.replace(".", ",")


def formatar_medida_mm(largura, altura):
    return f"{largura:g} × {altura:g} mm"
