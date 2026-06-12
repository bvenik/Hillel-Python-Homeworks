from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import User
from .forms import RegistrationForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('home')
                else:
                    error_message = "Incorrect username or password."
            except User.DoesNotExist:
                error_message = "Incorrect username or password."
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def home_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    return render(request, 'auth/home.html', {'username': request.session.get('username')})