from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration and automatically log in upon success.

    :param request: HTTP request object containing form data.
    :return: HTTP response rendering the registration form or redirecting to the protected view.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('protected')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user authentication and login.

    :param request: HTTP request object containing credentials.
    :return: HTTP response rendering the login form or redirecting to the protected view.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('protected')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Log out the current user.

    :param request: HTTP request object.
    :return: HTTP response redirecting to the login page.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def protected_view(request: HttpRequest) -> HttpResponse:
    """
    Render a protected page accessible only to authenticated users.

    :param request: HTTP request object.
    :return: HTTP response rendering the protected page.
    """
    return render(request, 'accounts/protected.html')


def xss_demo_view(request: HttpRequest) -> HttpResponse:
    """
    Demonstrate Cross-Site Scripting (XSS) vulnerability and Django's template protection.

    :param request: HTTP request object containing the search parameter.
    :return: HTTP response rendering the XSS demo page.
    """
    user_input = request.GET.get('search', '')
    return render(request, 'accounts/xss_demo.html', {'user_input': user_input})


def secure_sql_query(username_to_search: str) -> list[tuple]:
    """
    Execute a secure parameterized SQL query to prevent SQL injection.

    :param username_to_search: The username to search for in the database.
    :return: A list of tuples containing the query results.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, username FROM auth_user WHERE username = %s",
            [username_to_search]
        )
        result = cursor.fetchall()
    return result
