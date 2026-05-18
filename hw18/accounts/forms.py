from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new user with password confirmation and unique email validation.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """
        Validates that the provided email address is unique.

        :return: Cleaned email string.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        """
        Validates that the password and confirm_password fields match.

        :return: Dictionary of cleaned data.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Form for updating extended user profile data, including avatar size validation.
    """

    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_avatar(self):
        """
        Validates that the uploaded avatar image does not exceed 2 megabytes.

        :return: Cleaned avatar file object.
        """
        avatar = self.cleaned_data.get('avatar', False)
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 2mb ).")
            return avatar
        return avatar


class PasswordChangeForm(forms.Form):
    """
    Custom form for changing a user password, validating current and new credentials.
    """
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        """
        Initializes the form with the requesting user instance.

        :param user: The User instance attempting to change the password.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        """
        Validates that the provided current password matches the user's actual password.

        :return: Cleaned current password string.
        """
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError("Incorrect current password.")
        return current_password

    def clean(self):
        """
        Validates that new passwords match and differ from the current password.

        :return: Dictionary of cleaned data.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        current_password = cleaned_data.get("current_password")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "New passwords do not match.")

        if new_password and current_password and new_password == current_password:
            self.add_error('new_password', "New password must be different from the current one.")

        return cleaned_data
