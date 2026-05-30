import datetime
from django import forms
from django.utils import timezone


class TaskForm(forms.Form):
    """
    Form for creating a new task.
    """
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    due_date = forms.DateField(required=True)

    def clean_due_date(self) -> datetime.date:
        """
        Validate that the due date is not in the past.

        :return: The validated due date.
        :raises forms.ValidationError: If the date is in the past.
        """
        due_date: datetime.date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date
