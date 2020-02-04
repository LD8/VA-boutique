from django.urls import path
from . import views

app_name = 'boutique'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('women/', views.ItemListView.as_view(template_name = 'boutique/items.html'), name='women-all'),
    path('men/', views.ItemListView.as_view(template_name = 'boutique/items.html'), name='men-all'),

]
