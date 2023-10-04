from django.urls import path
from exames import views

urlpatterns = [
    path("solicitar_exames/", views.solicitar_exames, name="solicitar_exames")
]
