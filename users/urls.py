from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import *

urlpatterns = [
    path('signup/',create_user,name='create-user'),
    path('login/',LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/<str:username>/',view_profile.as_view(),name='profile-detail'),
    path('profile/<str:username>/update',update_profile,name='profile'),
]