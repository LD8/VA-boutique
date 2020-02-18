from django.contrib.auth import views as auth_views
from boutique.models import Category
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # to customise login view
    path('login/', auth_views.LoginView.as_view(extra_context = {'categories': Category.objects.get_categories_with_item()})),
    # path('login/', views.NewLoginView.as_view()),

    # to customise default logout view
    path('logout/', auth_views.LogoutView.as_view(), {'categories': Category.objects.get_categories_with_item()}),

    # include django authentication urls
    path('', include('django.contrib.auth.urls')),
    
    # the registration url
    path('register/', views.RegisterView.as_view(), name='register'),

    # user's profile page
    path('profile/<int:pk>-<str:slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>-<str:slug>/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    
]