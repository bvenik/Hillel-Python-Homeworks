from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the main page of the chat application.
    :param request: HTTP request object
    :return: HTTP response with the index template
    """
    return render(request, 'chat/index.html')


def register_user(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration. Creates a user, logs them in, and redirects.
    :param request: HTTP request object
    :return: redirect HTTP response to the main chat page
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                messages.success(request, f"Registered and logged in as {username}!")
        else:
            messages.error(request, "Invalid username or password.")
    return redirect('index')


def login_user(request: HttpRequest) -> HttpResponse:
    """
    Authenticates and logs in a user, then redirects to the main chat page.
    :param request: HTTP request object
    :return: redirect HTTP response to the main chat page
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in as {username}!")
        else:
            messages.error(request, "Invalid credentials.")
    return redirect('index')


def logout_user(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user and redirects to the main chat page.
    :param request: HTTP request object
    :return: redirect HTTP response to the main chat page
    """
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')
