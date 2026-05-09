from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
import random

def home(request):
    """
    Renders the home page with a welcome message.
    Uses 'upper' and 'lower' filters for text formatting.
    """
    return render(request, 'home.html')

def about(request):
    """
    Renders the 'About Us' page.
    Passes company history and current date for testing 'date', 'truncatechars', and 'safe' filters.
    """
    context = {
        'last_updated': datetime.now(),
        'company_history': "Ми — молода компанія з 4 людей, з креативним мишленням, чудовими амбіціями, та скаженими ідеями.",
        'mission_html': "<strong>Наша мета:</strong> розповсюдити свій продукт кожній людині."
    }
    return render(request, 'about.html', context)

class ContactView(TemplateView):
    """
    Class-based view for the contact page.
    Implements 'yesno' filter logic and 'default' value for missing data.
    """
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_open'] = random.choice([True, False])
        context['phone'] = ""
        return context

class ServiceView(TemplateView):
    """
    Class-based view for the services page.
    Demonstrates usage of 'length', 'slice', and 'pluralize' filters on a list.
    """
    template_name = 'services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = [
            'Розробка сайтів',
            'Дизайн інтерфейсів',
            'QA тестування',
            'SEO просування',
            'SMM менеджмент'
        ]
        return context