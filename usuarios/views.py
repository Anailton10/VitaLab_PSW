from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login


def cadastro(request):
    if request.method == 'GET':  # requisição por link
        return render(request, 'cadastro.html')
    elif request.method == 'POST':  # requisição pelo form
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'As senhas são diferentes')
            return redirect('/usuarios/cadastro/')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 'Senha menor que 6 caracteres')
            return redirect('/usuarios/cadastro/')

        try:
            # TODO: validar se o username do usario não existe
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha
            )
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema, contate um administrador')
            return redirect('/usuarios/cadastro/')
        messages.add_message(request, constants.SUCCESS,
                             'Cadastro realizado com sucesso!!')
        return redirect('/usuarios/cadastro/')


def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            login(request, user)
        else:
            messages.add_message(request, constants.ERROR,
                                 'Username ou senha invalidos')
            return redirect('/usuarios/login')
        return HttpResponse(f'{username} - {senha}')
