import os

from django.shortcuts import render, redirect
from django.conf import settings
from controle.forms import *
from controle.functions import *
from django.contrib import messages

# Create your views here.
from controle.models import Transacao


def index(request):
    t = Transacao.objects.all().order_by('-data_transacao')
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            excel = request.FILES['file']
            arquivo = get_csv(excel)
            if not get_length(arquivo):
                messages.error(request, "Arquivo vazio !", extra_tags='alert alert-danger')
                return redirect(index)
            valida_vazio = is_empty(arquivo)
            valida_data = validate_date(valida_vazio)
            if get_duplicado(valida_data) != 0:
                messages.error(request, "Transação Duplicada !", extra_tags='alert alert-danger')
                return redirect(index)
            for v in valida_data:
                Transacao.objects.create(
                    banco_origem=v[0],
                    agencia_origem=v[1],
                    conta_origem=v[2],
                    banco_destino=v[3],
                    agencia_destino=v[4],
                    conta_destino=v[5],
                    valor=v[6],
                    data_transacao=v[7]
                    )
            form.save()
    data = {
        'transacao': t
    }
    return render(request, 'index.html', data)
