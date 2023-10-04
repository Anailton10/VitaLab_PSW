from django.contrib import admin
from .models import TipoExames,SolicitacaoExame, PedidosExame

admin.site.register(TipoExames)
admin.site.register(PedidosExame)
admin.site.register(SolicitacaoExame)