from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from controle.forms import FileForm
from controle.functions import *
from controle.models import Transacao, Usuario

from datetime import datetime


# Create your views here.

@login_required(login_url="login")
def index(request):
    t = Transacao.objects.all().order_by('-data_transacao')
    u = Usuario.objects.get(user=request.user.id)
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
                    user=u,
                    banco_origem=v[0],
                    agencia_origem=v[1],
                    conta_origem=v[2],
                    banco_destino=v[3],
                    agencia_destino=v[4],
                    conta_destino=v[5],
                    valor=v[6],
                    data_transacao=v[7]
                )
    data = {
        'transacao': t
    }
    return render(request, 'index.html', data)


@login_required(login_url="login")
def detalhes(request, pk):
    t = Transacao.objects.get(pk=pk)

    data = {
        'transacao': t
    }

    return render(request, 'detalhes.html', data)


@login_required(login_url="login")
def suspeitas(request):
    pesquisa = f'{datetime.now().year}-{datetime.now().month:02}'
    data = {
        'pesquisa': pesquisa
    }

    if request.GET.get('pesquisa'):
        pesquisa = request.GET.get('pesquisa')
        ano, mes = pesquisa.split('-')
        data.update({'pesquisa': pesquisa})
        if Transacao.objects.filter(data_transacao__month=mes, data_transacao__year=ano).exists():
            v = Transacao.objects.filter(data_transacao__month=mes, data_transacao__year=ano)
            transacao_suspeita = v.filter(valor__gte=100_000)
            conta_suspeita = get_conta_suspeita(ano, mes)
            agencia_suspeita = get_agencia_suspeita(ano, mes)
            data.update({
                't_suspeita': transacao_suspeita,
                'c_suspeita': conta_suspeita,
                'a_suspeita': agencia_suspeita
            })
        else:
            messages.error(request, "Não há nenhuma transação suspeita !", extra_tags='alert alert-danger')

    return render(request, 'suspeitas.html', data)
