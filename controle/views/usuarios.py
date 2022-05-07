from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from controle.models import Usuario
import random


@login_required(login_url="login")
def usuarios(request):
    u = Usuario.objects.all().order_by('-id')
    data = {
        'usuarios': u
    }
    return render(request, 'usuarios/usuarios.html', data)


@login_required(login_url="login")
def cria_usuario(request):
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
            print(EMAIL_HOST_USER)
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
    return render(request, 'usuarios/novo.html')


@login_required(login_url="login")
def deleta_usuario(request, pk):
    u = Usuario.objects.get(pk=pk)
    user = u.user
    user.is_active = False
    user.save()
    return redirect('usuarios')


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
