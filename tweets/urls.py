from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('login/twitter', views.login, name = 'login'),
    path('auth/twitter', views.auth, name = 'auth'),
    path('profile', views.profile, name = 'profile'),
    path('logout', views.logout, name = 'logout'),
    path('search', views.search, name = 'search')
]
