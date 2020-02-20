from django.urls import path, include
from . import views

app_name = 'wishlist'
urlpatterns = [

    # disply the wish list of a particular profile
    path('<str:slug>/', views.wish_list, name='wish-list'),
    
    # add/delete an item to the wish list
    path('del-wish/<int:item_pk>/', views.del_wish, name='del-wish'),
    path('add-wish/<int:item_pk>/', views.add_wish, name='add-wish'),

]