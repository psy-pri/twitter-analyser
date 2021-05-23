from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/twitter', views.login, name = 'login'),
    path('auth/twitter', views.auth, name = 'auth'),
    path('profile', views.profile, name = 'profile')
]
