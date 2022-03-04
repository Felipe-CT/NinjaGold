from django.urls import path
from . import views

urlpatterns = [

    path('process_money', views.process_money),
    path('procesar', views.procesar),
    path('home', views.home),
]
