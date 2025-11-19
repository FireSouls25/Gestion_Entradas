from django.urls import path, reverse_lazy
from .views import login_view, register_view, logout_view, client_list_view, settings_view, delete_account_view
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('users/', client_list_view, name='user-list'),
    path('settings/', settings_view, name='settings'),
    path('delete-account/', delete_account_view, name='delete-account'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html', success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
