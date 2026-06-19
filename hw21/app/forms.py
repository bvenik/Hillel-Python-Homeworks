from django import forms
from django.utils import timezone

class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(required=False)
    due_date = forms.DateField()

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Date can not be in past.")
        return due_date