from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('login/', views.login_view, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout/', views.logout_view, name='logout'),

    # include django authentication urls
    path('', include('django.contrib.auth.urls')),
    
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('register/', views.register_view, name='register'),

    # user's profile page
    path('profile/<int:pk>-<str:slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>-<str:slug>/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    
]