import re
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, ProjectTask


class CustomSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=()):
        default_attrs = {'class': 'custom-task-select',
                         'style': 'border: 2px solid #00c853; padding: 5px; border-radius: 4px;'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs, choices)


class HexColorField(forms.CharField):
    def clean(self, value):
        value = super().clean(value)
        if value and not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise ValidationError("Invalid hex color.")
        return value


class ProjectTaskForm(forms.ModelForm):
    tag_color = HexColorField(required=False, label="HEX color code")

    class Meta:
        model = ProjectTask
        fields = ['title', 'status_code', 'description', 'tag_color']
        widgets = {
            'status_code': CustomSelectWidget(choices=[
                ('NEW', 'New'),
                ('PROCESSING', 'Processing'),
                ('URGENT', 'Urgent')
            ])
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise ValidationError("Title must have at least 5 characters.")
        return title


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.startswith('+380'):
            raise ValidationError("Номер телефону повинен обов'язково починатися з українського коду +380.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
