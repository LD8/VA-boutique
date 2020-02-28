from django.urls import path
from . import views

app_name = 'vip'
urlpatterns = [
    # path('create-order/', views.VipOrderCreateView.as_view(), name='create-vip-order'),
    path('create-order/', views.create_vip_order, name='create-vip-order'),
    path('order/<str:ref>/', views.show_vip_order, name='vip-order'),
    # path('order/<str:ref>/', views.VipOrderDetailView.as_view(), name='vip-order'),
]