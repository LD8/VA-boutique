from django.urls import path
from . import views

app_name = 'vip'
urlpatterns = [
    path('create-order/', views.VipOrderCreateView.as_view(), name='vip-create-order'),
    path('order/<str:slug>/', views.VipOrderDetailView.as_view(), name='vip-order'),
]