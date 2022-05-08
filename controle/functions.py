import csv
from io import StringIO
from datetime import datetime

from django.db.models import Sum, F

from controle.models import Transacao


def get_csv(file):
    f = StringIO(file.read().decode('utf-8'))
    t = [line for line in csv.reader(f)]
    return t


def is_empty(file):
    list = []
    for f in file:
        list.append(f)  # Adiciona todos na lista
        for i in f:
            if i == "":  # Se estiver vazio
                list.remove(f)  # Remove da lista se estiver vazio
    return list


def validate_date(file):
    list = []
    primeira_data = get_first_date(file)

    for v in file:
        data = get_date(v)
        if primeira_data == data:
            list.append(v)  # Adiciona os items que tem a mesma data
    return list


def get_date(file):
    data = datetime.fromisoformat(file[-1]).date()  # Separa a data
    return data


def get_first_date(file):
    list_data = []
    for f in file:
        data = get_date(f)
        list_data.append(data)
    return list_data[0]  # Retorna a primeira data


def get_length(file):
    if all(file):
        return True
    else:
        return False


def get_duplicado(file):
    data = get_first_date(file)

    v = Transacao.objects.filter(data_transacao__date=data)

    return len(v)


def get_conta_suspeita(ano, mes):
    transacoes = Transacao.objects.filter(data_transacao__month=mes,
                                          data_transacao__year=ano)

    c_origem = (transacoes.values('banco_origem', 'agencia_origem', 'conta_origem')
                .annotate(valor_suspeito=Sum('valor'),
                          banco=F('banco_origem'),
                          agencia=F('agencia_origem'),
                          conta=F('conta_origem'))
                .filter(valor_suspeito__gt=1_000_000))

    c_destino = (transacoes.values('banco_destino', 'agencia_destino', 'conta_destino')
                 .annotate(valor_suspeito=Sum('valor'),
                           banco=F('banco_destino'),
                           agencia=F('agencia_destino'),
                           conta=F('conta_destino'))
                 .filter(valor_suspeito__gt=1_000_000))

    for c in c_origem:
        c.update({'tipo_movimentacao': 'Saída'})

    for c in c_destino:
        c.update({'tipo_movimentacao': 'Entrada'})

    conta_suspeita = list(c_origem) + list(c_destino)

    return conta_suspeita


def get_agencia_suspeita(ano, mes):
    transacoes = Transacao.objects.filter(data_transacao__month=mes,
                                          data_transacao__year=ano)

    a_origem = (transacoes.values('banco_origem', 'agencia_origem')
                .annotate(valor_suspeito=Sum('valor'),
                          banco=F('banco_origem'),
                          agencia=F('agencia_origem'))
                .filter(valor_suspeito__gt=1_000_000_000))

    a_destino = (transacoes.values('banco_destino', 'agencia_destino')
                 .annotate(valor_suspeito=Sum('valor'),
                           banco=F('banco_destino'),
                           agencia=F('agencia_destino'))
                 .filter(valor_suspeito__gt=1_000_000_000))

    for a in a_origem:
        a.update({'tipo_movimentacao': 'Saída'})

    for a in a_destino:
        a.update({'tipo_movimentacao': 'Entrada'})

    agencia_suspeita = list(a_origem) + list(a_destino)

    return agencia_suspeita
