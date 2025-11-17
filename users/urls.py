from django.urls import path
from .views import login_view, register_view, logout_view, client_list_view, settings_view, delete_account_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('clients/', client_list_view, name='client-list'),
    path('settings/', settings_view, name='settings'),
    path('delete-account/', delete_account_view, name='delete-account'),
]
