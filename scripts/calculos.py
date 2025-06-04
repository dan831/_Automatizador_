import pandas as pd
from datetime import datetime
import scripts.calculos as calculos

def dias_trabalhados_13(data_admissao_str, data_desligamento_str):
    data_admissao = datetime.strptime(data_admissao_str, '%d/%m/%Y')
    data_desligamento = datetime.strptime(data_desligamento_str, '%d/%m/%Y')
    
    if data_admissao.year == data_desligamento.year:
        dias_trabalhados = (data_desligamento - data_admissao).days + 1
    else:
        data_inicio_ano = datetime(data_desligamento.year, 1, 1)
        dias_trabalhados = (data_desligamento - data_inicio_ano).days + 1

    return dias_trabalhados


def dias_trabalhados_ferias(data_admissao_str, data_desligamento_str):
    data_admissao = datetime.strptime(data_admissao_str, '%d/%m/%Y')
    data_desligamento = datetime.strptime(data_desligamento_str, '%d/%m/%Y')

    dias_trabalhados = (data_desligamento - data_admissao).days + 1

    if data_admissao.year == data_desligamento.year:
        return dias_trabalhados
    elif data_admissao.year < data_desligamento.year and dias_trabalhados <= 365:
        return dias_trabalhados
    elif 365 <= dias_trabalhados <= 730:
        return dias_trabalhados - 365
    elif dias_trabalhados > 730:
        return 365
    else:
        return dias_trabalhados

def dias_trabalhados_ferias_não_gozadas(data_admissao_str, data_desligamento_str):
    data_admissao = datetime.strptime(data_admissao_str, '%d/%m/%Y')
    data_desligamento = datetime.strptime(data_desligamento_str, '%d/%m/%Y')

    dias_trabalhados = (data_desligamento - data_admissao).days + 1

    if dias_trabalhados <= 365:
        return 0
    elif dias_trabalhados > 365:
        return dias_trabalhados - 365
    else:
        return dias_trabalhados

def dias_ferias_nao_gozadas(data_admissao_str, data_desligamento_str, ferias_gozadas):
    data_admissao = datetime.strptime(data_admissao_str, '%d/%m/%Y')
    data_desligamento = datetime.strptime(data_desligamento_str, '%d/%m/%Y')

    dias_trabalhados = (data_desligamento - data_admissao).days

    if dias_trabalhados < 365:
        return 0
    else:
        dias_nao_gozados = 30 - ferias_gozadas
        return max(dias_nao_gozados, 0)
    
def ferias_gozadas(base_calc, cet_calc, dias_trabalhados_ferias, dias_gozados):
    if dias_trabalhados_ferias < 365:  
        return 0.0
    else:
        return round(((base_calc + cet_calc) / 30) * (dias_gozados), 2)

def calcular_13_proporcional(recebimento_ultimo, dias_trabalhados_13):
    return round((recebimento_ultimo / 365) * dias_trabalhados_13, 2)

def ferias_proporcionais(recebimento_ultimo, dias_trabalhados_ferias):
    return round((recebimento_ultimo / 365) * dias_trabalhados_ferias, 2)

def terco_ferias(ferias_proporcionais):
    return round(ferias_proporcionais / 3, 2)

def indenizacao_total(valor_13, valor_ferias_proporcionais, valor_ferias_nao_gozadas, valor_terco_ferias):
    total = 0
    total += valor_13 if isinstance(valor_13, (int, float)) else 0
    total += valor_ferias_proporcionais if isinstance(valor_ferias_proporcionais, (int, float)) else 0
    total += valor_ferias_nao_gozadas if isinstance(valor_ferias_nao_gozadas, (int, float)) else 0
    total += valor_terco_ferias if isinstance(valor_terco_ferias, (int, float)) else 0
    return round(total, 2)



