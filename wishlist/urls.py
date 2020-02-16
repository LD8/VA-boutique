from django.urls import path, include
from . import views

app_name = 'wishlist'
urlpatterns = [

    path('<str:slug>/', views.WishListView.as_view(), name='wish-list'),

]