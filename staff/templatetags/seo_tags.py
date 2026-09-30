import html
import re

from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter
def plain_summary(value, length=155):
    text = html.unescape(strip_tags(html.unescape(str(value or ''))))
    text = re.sub(r'\s+', ' ', text).strip()
    length = int(length)
    if len(text) > length:
        text = text[:length].rsplit(' ', 1)[0] + '…'
    return text
