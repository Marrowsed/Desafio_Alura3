import csv
from io import StringIO
from datetime import datetime

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
    return list_data[0] #Retorna a primeira data


def get_length(file):
    if all(file):
        return True
    else:
        return False

def get_duplicado(file):
    data = get_first_date(file)

    v = Transacao.objects.filter(data_transacao__date=data)

    return len(v)
