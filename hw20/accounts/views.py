from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import connection


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('protected')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('protected')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def protected_view(request):
    return render(request, 'accounts/protected.html')


def xss_demo_view(request):
    user_input = request.GET.get('search', '')
    return render(request, 'accounts/xss_demo.html', {'user_input': user_input})


def secure_sql_query(username_to_search):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, username FROM auth_user WHERE username = %s", [username_to_search])
        result = cursor.fetchall()
    return result
