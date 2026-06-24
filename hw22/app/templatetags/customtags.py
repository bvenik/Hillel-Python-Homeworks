from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='add_alert_icon')
def add_alert_icon(value):
    if value == 'URGENT':
        return f"⚠️ {value}"
    return f"📌 {value}"


@register.simple_tag(name='current_time_formatted')
def current_time_formatted(format_string):
    return timezone.now().strftime(format_string)