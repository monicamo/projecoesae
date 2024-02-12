from datetime import datetime, timedelta

meses = {
    'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
    'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
}

def gerar_data_referencia(descricao):
    # Se a descrição tiver o formato "MesAA/MesAA"
    if '/' in descricao:
        # Dividir a descrição em seus componentes
        inicio_mes, inicio_ano = descricao.split('/')[1][:3], int(descricao.split('/')[1][3:])
        fim_mes, fim_ano = descricao.split('/')[0][:3], int(descricao.split('/')[0][3:])

        # Adicionar 2000 ao ano se for de dois dígitos
        if inicio_ano < 100:
            inicio_ano += 2000
        if fim_ano < 100:
            fim_ano += 2000

        # Converta o mês de texto para o número correspondente
        inicio_mes_num = meses[inicio_mes.lower()]
        fim_mes_num = meses[fim_mes.lower()]

        # Gere as datas de início e término
        data_inicio = datetime(inicio_ano, inicio_mes_num, 1)
        data_fim = datetime(fim_ano, fim_mes_num, 1)

    # Se a descrição tiver apenas o formato de ano em 4 dígitos
    else:
        # Extrair o ano
        ano = int(descricao)

        # Determinar a data de início e fim como o primeiro e o último dia do ano
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)

    # Ajuste para o período de 12 meses
    if descricao.endswith('s'):
        data_inicio = data_inicio - timedelta(days=365)

    return data_inicio, data_fim

