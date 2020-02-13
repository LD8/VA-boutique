from django.urls import path
from . import views

app_name = 'boutique'
urlpatterns = [
    # show index page
    path('', views.IndexView.as_view(), name='index'),
    
    # search
    path('search/', views.SearchView.as_view(), name='search'),

    # show a specific item
    path('item_<int:pk>/', views.ItemDetailView.as_view(), name='item'), 
    # for DetailView to work, either pass in <pk> or specify in CBV `pk_url_kwargs = 'item_pk'`

    path('subcat_<int:subcategory_pk>/', views.CategoryListView.as_view(template_name="boutique/show_subcategory.html"), name='show-subcategory'),
    path('subcat_<int:subcategory_pk>/filter/', views.FilterCategoryListView.as_view(), name='filter-subcategory'),

    path('cat_<int:category_pk>/', views.CategoryListView.as_view(template_name="boutique/show_category.html"), name='show-category'),
    path('cat_<int:category_pk>/filter/', views.FilterCategoryListView.as_view(), name='filter-category'),

    path('<slug:gender>/', views.CategoryListView.as_view(template_name="boutique/show_all.html"), name='show-all'),
    path('<slug:gender>/filter/', views.FilterCategoryListView.as_view(template_name="boutique/show_all.html"), name='filter-all'),
]
