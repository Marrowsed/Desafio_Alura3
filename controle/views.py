import bcrypt
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from controle.decorator import unauthenticated_user
from controle.forms import *
from controle.functions import *
from controle.models import Transacao, Usuario


# Create your views here.

@login_required(login_url="login")
def index(request):
    t = Transacao.objects.all().order_by('-data_transacao')
    u = Usuario.objects.get(user=request.user)
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
            form.save()
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


# Views de acesso
@unauthenticated_user
def entrar(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        username = User.objects.get(email=email.lower()).username
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Usuário ou senha incorreto', extra_tags="alert alert-danger")
    return render(request, 'acessos/login.html')


def sair(request):
    logout(request)
    return redirect("index")


@unauthenticated_user
def cadastro(request):
    return render(request, 'acessos/login.html')


# Views do usuário
@login_required(login_url="login")
def usuarios(request):
    u = Usuario.objects.all().order_by('-id')
    data = {
        'usuarios': u
    }
    return render(request, 'usuarios/usuarios.html', data)

@login_required(login_url="login")
def cria_usuario(request):
    pass

@login_required(login_url="login")
def deleta_usuario(request):
    pass

@login_required(login_url="login")
def edita_usuario(request, pk):
    u = Usuario.objects.get(pk=pk)
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        if Usuario.objects.filter(email=email).exists():
            messages.info(request, 'E-mail em uso !', extra_tags="alert alert-danger")
        else:
            u.nome = nome
            u.email = email
            u.save()
            return redirect('usuarios')

    data = {
        'usuario': u

    }
    return render(request, 'usuarios/edita.html', data)
