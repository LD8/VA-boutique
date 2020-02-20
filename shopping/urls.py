from django.urls import path, include
from . import views

app_name = 'shopping'
urlpatterns = [
    # actions: access shopping-bag (detailview),
    path('shopping-bag/', views.shopping_bag, name='shopping-bag'),
    # add oder_item to bag,
    path('add/<int:item_pk>/', views.add_to_bag, name='add-to-bag'),
    # delete order_item from bag,
    path('del/<int:order_item_pk>/', views.del_from_bag, name='del-from-bag'),
    
    # generate order ref, fill in forms, comfirm, sending an email to admin
    path('handle-order/', views.handle_order, name='handle-order'),
    # handle buy now and display buy now
    path('handle-order/buy-now/<int:item_pk>/', views.buy_now, name='buy-now'),
    path('handle-order/buy-now/<int:item_pk>/registered/', views.buy_now_registered, name='buy-now-registered'),
    path('handle-order/buy-now/<int:item_pk>/<str:order_ref_number>/', views.buy_now_order, name='buy-now-order'),

    # show all placed orders
    path('orders/', views.OrderListView.as_view(), name='show-orders'),
    # a placed order detail page
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='show-order'),

]
