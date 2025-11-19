from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import UserProfile
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test

def is_organizer_or_attendee(user):
    return user.is_authenticated and (user.userprofile.role == 'organizer' or user.userprofile.role == 'attendee')

@login_required
@user_passes_test(is_organizer_or_attendee)
def client_list_view(request):
    clients = UserProfile.objects.filter(role='client')
    attendees = UserProfile.objects.filter(role='attendee')
    return render(request, 'users/user_list.html', {'clients': clients, 'attendees': attendees})

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:settings')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/settings.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('users:login')
    return redirect('users:settings')

@never_cache
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Usuario o contraseña inválidos.', extra_tags='login_error')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.', extra_tags='login_error')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')
