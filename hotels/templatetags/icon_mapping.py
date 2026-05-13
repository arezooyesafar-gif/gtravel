from django import template
from ..icon_mapping import SERVICE_ICONS

register = template.Library()

@register.filter
def get_icon_name(service_name):
    return SERVICE_ICONS.get(service_name, 'check_circle')