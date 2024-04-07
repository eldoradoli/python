from django.urls import path
from . import views
from .views import welcome

app_name = 'api'
urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('login',views.login, name='login'),
    path('check_user',views.check_user_exists, name='check_user'),
    path('check_username',views.check_username, name='check_username'),
    path('save_user', views.save_user, name='save_user')
]