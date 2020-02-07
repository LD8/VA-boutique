from django.urls import path
from . import views

app_name = 'boutique'
urlpatterns = [
    # show index page
    path('', views.IndexView.as_view(), name='index'),
    
    # show a specific item
    path('item_<int:item_pk>/', views.ItemDetailView.as_view(), name='item'),

    # show categories of products for men or women
    path('<slug:gender>/', views.CategoryListView.as_view(), name='show-all'),

    # show a specific category for men or women
    path('<slug:gender>/cat_<int:category_pk>/', views.CategoryListView.as_view(), name='category'),

    # show a specific subcategory under a specific category for men or women
    path('<slug:gender>/cat_<int:category_pk>/subcat_<int:subcategory_pk>/', views.CategoryListView.as_view(), name='subcategory'),

]
