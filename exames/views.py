from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from exames.models import TipoExames


@login_required  # apenas usuarios logados poderam acessar essa views
def solicitar_exames(request):
    tipos_exames = TipoExames.objects.all()
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html', {"tipos_exames": tipos_exames})
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TipoExames.objects.filter(
            id__in=exames_id)  # Filtrando pelo ID

        preco_total = 0
        for i in solicitacao_exames:
            preco_total += i.preco

    return render(request, 'solicitar_exames.html', {"tipos_exames": tipos_exames})
