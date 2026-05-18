from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm


def register_view(request):
    """
    Handles user registration and automatic login upon success.

    :param request: HttpRequest object.
    :return: HttpResponse rendering the registration template or redirecting.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('profile_view')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    Displays the profile information of the currently authenticated user.

    :param request: HttpRequest object.
    :return: HttpResponse rendering the profile view template.
    """
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})


@login_required
def edit_profile_view(request):
    """
    Handles the updating process of the user's profile data and avatar.

    :param request: HttpRequest object.
    :return: HttpResponse rendering the profile edit template or redirecting.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    """
    Handles password changes and updates the session authentication hash.

    :param request: HttpRequest object.
    :return: HttpResponse rendering the password change template or redirecting.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect('profile_view')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
