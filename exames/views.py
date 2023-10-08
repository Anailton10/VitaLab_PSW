from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from exames.models import TipoExames, PedidosExame, SolicitacaoExame
from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages


@login_required  # apenas usuarios logados poderam acessar essa views
def solicitar_exames(request):
    tipos_exames = TipoExames.objects.all()
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html',
                      {"tipos_exames": tipos_exames})
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TipoExames.objects.filter(
            id__in=exames_id)  # Filtrando pelo ID

        preco_total = 0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco

        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames,
                                                         'solicitacao_exames': solicitacao_exames,
                                                         'preco_total': preco_total})


@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TipoExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExame(
        usuario=request.user,
        data=datetime.now()
    )
    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)

    pedido_exame.save()
    messages.add_message(request, constants.SUCCESS,
                         'Pedido de exame realizado com sucesso!')
    return redirect('/exames/ver_pedidos/')
