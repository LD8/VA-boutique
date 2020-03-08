from django.urls import path
from . import views

app_name = 'boutique'
urlpatterns = [
    # show index page
    path('', views.IndexView.as_view(), name='index'),
    
    path('sales/', views.SalesListView.as_view(), name='sales'),
    
    # general search, text input
    path('search/', views.SearchView.as_view(), name='search'),

    # for DetailView to work, either pass in <pk> or specify in CBV `pk_url_kwargs = 'item_pk'`
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item'), 

    path('cat/subcat/<int:pk>/', views.show_subcategory, name='show-subcategory'),

    path('cat/<int:pk>/', views.show_category, name='show-category'),

    path('filtered/subcat/<int:pk>/', views.filter_item, name='filter'),
    path('filtered/all/', views.filter_item, name='filter-all'),

    path('<str:gender>/', views.show_all, name='show-all'),
    
]
