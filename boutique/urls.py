from django.urls import path
from . import views

app_name = 'boutique'
urlpatterns = [
    path('', views.index, name='index'),
]
