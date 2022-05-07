from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth

from controle.decorator import unauthenticated_user
from controle.models import Usuario
import random


@unauthenticated_user
def entrar(request):
    if request.method == 'POST':
        print(EMAIL_HOST_USER)
        email = request.POST['email']
        senha = request.POST['senha']
        user = auth.authenticate(request, username=email, password=senha)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Usuário ou senha incorreto', extra_tags="alert alert-danger")
    return render(request, 'acessos/login.html')


def sair(request):
    logout(request)
    return redirect("index")


@unauthenticated_user
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['username']
        email = request.POST['email']
        if nome == "" or email == "":
            messages.error(request, "Todos os campos precisam ser preenchidos !", extra_tags='alert alert-danger')
        if User.objects.filter(email=email).exists():
            messages.error(request, "E-mail já existe !", extra_tags='alert alert-danger')
        senha = str(random.randint(100000, 999999))
        try:
            send_mail(
                'Parabéns !',
                f'Seu cadastro foi realizado com sucesso! Sua senha é {senha}.',
                EMAIL_HOST_USER,
                email,
                fail_silently=False
            )
        except:
            return HttpResponse('Erro no envio do e-mail')
        else:
            user = User.objects.create_user(
                first_name=nome,
                username=email,
                email=email,
                password=senha
            )
            usuario = Usuario.objects.create(
                user=user,
                nome=nome,
                email=email,
                senha=senha
            )
            user.save()
            usuario.save()

    return render(request, 'acessos/cadastro.html')
