from django.urls import path
from . import views

app_name = 'boutique'
urlpatterns = [
    # show index page
    path('', views.IndexView.as_view(), name='index'),
    
    # general search, text input
    path('search/', views.SearchView.as_view(), name='search'),

    path('item_<int:pk>/', views.ItemDetailView.as_view(), name='item'), 
    # for DetailView to work, either pass in <pk> or specify in CBV `pk_url_kwargs = 'item_pk'`

    path('<str:gender>/subcat_<int:subcategory_pk>/', views.CategoryListView.as_view(), name='show-subcategory'),

    path('<str:gender>/cat_<int:category_pk>/', views.CategoryListView.as_view(), name='show-category'),

    path('<str:gender>/', views.CategoryListView.as_view(), name='show-all'),
    # path('show-all/', views.CategoryListView.as_view(), name='show-all'),
]
