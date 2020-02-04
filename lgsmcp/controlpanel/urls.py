from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cp-index'),  # Index page with information about gameserver
    path('lgsm/', views.lgsm, name='cp-lgsm'),
    path('login/', views.loginToGameserver, name='cp-login'),  # Allow to log into gameserver
    path('logout/', views.logoutOfGameserver, name='cp-logout'),  # Allow to log out of gameserver
]