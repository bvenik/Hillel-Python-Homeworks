import string
from django import forms
from django.core.exceptions import ValidationError
from .models import User


class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            password = cleaned_data.get("password")
            password_confirm = cleaned_data.get("password_confirm")

            if password and password_confirm and password != password_confirm:
                raise ValidationError("Passwords don't match")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Username must contain at least 3 characters")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password and len(password) < 8:
            raise ValidationError("Password must contain at least 8 characters.")

        if password and not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least 1 letter.")

        if password and not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least 1 digit.")

        if password and not any(char in string.punctuation for char in password):
            raise ValidationError("Password must contain at least 1 special character.")

        return password


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(min_length=3, widget=forms.PasswordInput())