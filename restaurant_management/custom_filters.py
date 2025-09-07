from django import template 
from django.utils import timezone
register = template.Library()
@register.simple_tag
def current_datetime(format_string = "%A,%B,%D,%Y,%I:%M,%p"):
    return timezone.now().strf_time(format_string)
    