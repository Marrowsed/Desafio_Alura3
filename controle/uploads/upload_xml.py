import xml.etree.ElementTree as ET
from datetime import datetime

from controle.models import Transacao, Usuario


def get_xml(file, request):
    xmldoc = ET.parse(file)
    root = xmldoc.getroot()
    transacao = root.findall('./transacao')
    primeira_transacao = transacao[0]

    data_str = primeira_transacao.find('./data').text[:10]
    data = datetime.strptime(data_str, '%Y-%m-%d').date()
    u = Usuario.objects.get(user=request.user.id)

    if not validate_data(data):
        for t in transacao:
            if validate(t, data):
                banco_origem = t.find('./origem/banco').text
                agencia_origem = t.find('./origem/agencia').text
                conta_origem = t.find('./origem/conta').text
                banco_destino = t.find('./destino/banco').text
                agencia_destino = t.find('./destino/agencia').text
                conta_destino = t.find('./destino/conta').text
                valor = float(t.find('./valor').text)
                data_transacao = datetime.strptime(t.find('./data').text,
                                                   '%Y-%m-%dT%H:%M:%S')
                t = Transacao.objects.create(
                    user=u,
                    banco_origem=banco_origem,
                    agencia_origem=agencia_origem,
                    conta_origem=conta_origem,
                    banco_destino=banco_destino,
                    agencia_destino=agencia_destino,
                    conta_destino=conta_destino,
                    valor=valor,
                    data_transacao=data_transacao
                )
                t.save()

def validate(dados, data_arquivo):
    try:
        data = datetime.strptime(dados.find('./data').text,
                                 '%Y-%m-%dT%H:%M:%S')

        if (data.year != data_arquivo.year or
                data.month != data_arquivo.month or
                data.day != data_arquivo.day):
            return False

        atributos = [
            './origem/banco',
            './origem/agencia',
            './origem/conta',
            './destino/banco',
            './destino/agencia',
            './destino/conta',
            './valor',
            './data'
        ]

        for atributo in atributos:
            if (dados.find(atributo) is None or
                    dados.find(atributo).text is None):
                return False

        return True

    except ValueError:
        return False


def validate_data(data):
    Transacao.objects.filter(data_transacao__date=data).exists()
