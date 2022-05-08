from django.db.models import Sum, F
from controle.models import Transacao


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
