from django.urls import path, include
from . import views

app_name = 'shopping'
urlpatterns = [

    # shopping bag
    path('shopping-bag/<str:slug>/', views.ShoppingBagView.as_view(), name='shopping-bag'),

    
]