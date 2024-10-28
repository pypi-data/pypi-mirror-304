from datetime import datetime, timedelta
import calendar
import holidays

from datetime import datetime, timedelta
import calendar
import holidays

def calcular_codigo_dolar(data=None):
    # Mapeamento de códigos para meses (janeiro é 'G', dezembro é 'F')
    month_codes = {
        1: 'G', 2: 'H', 3: 'J', 4: 'K', 5: 'M', 6: 'N',
        7: 'Q', 8: 'U', 9: 'V', 10: 'X', 11: 'Z', 12: 'F'
    }
    
    # Usar a data fornecida ou a data atual
    if data is None:
        data = datetime.now()
    else:
        data = datetime.strptime(data, '%Y-%m-%d')
        
    ano_atual = data.year
    ano = str(ano_atual)[-2:]  # Últimos dois dígitos do ano

    # Obter os feriados nacionais do Brasil para o ano atual
    feriados_nacionais = holidays.BR(years=[ano_atual])

    # Adicionar feriados específicos (vésperas)
    feriados_especiais = [
        datetime(ano_atual, 12, 24),  # Véspera de Natal
        datetime(ano_atual, 12, 31),  # Véspera de Ano Novo
    ]

    # Combinar com os feriados nacionais
    feriados = set(feriados_nacionais.keys()) | set(feriados_especiais)

    # Função para encontrar o último dia útil do mês, considerando feriados
    def ultimo_dia_util(mes, ano):
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        data_util = datetime(ano, mes, ultimo_dia)
        while data_util.weekday() >= 5 or data_util in feriados:
            data_util -= timedelta(days=1)
        return data_util

    ultimo_dia_util_mes = ultimo_dia_util(data.month, data.year)

    # Determina o código: se data >= último dia útil do mês, avança para o próximo mês
    if data >= ultimo_dia_util_mes:
        # Muda para o próximo mês
        mes_dolar = data.month + 1 if data.month < 12 else 1
        if mes_dolar == 1:
            ano_dolar = str(ano_atual + 1)[-2:]  # Incrementa o ano se for janeiro
        else:
            ano_dolar = ano
    else:
        # Usa o código do mês atual
        mes_dolar = data.month
        ano_dolar = ano

    codigo_dolar = f"WDO{month_codes[mes_dolar]}{ano_dolar}"
    return codigo_dolar







