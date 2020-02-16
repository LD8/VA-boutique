from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # include django authentication urls
    path('', include('django.contrib.auth.urls')),

    # the registration url
    # path('register/', views.register, name='register'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # user's profile page
    path('profile/', views.profile, name='profile'),
    
]