from django import template

from ..models import ObjectStamp

register = template.Library()


@register.simple_tag
def last_change(instance):
    if instance is None or not getattr(instance, 'pk', None):
        return None
    label = '%s.%s' % (instance._meta.app_label, instance._meta.model_name)
    return ObjectStamp.objects.filter(model_label=label, object_id=str(instance.pk)).first()


@register.filter
def person_name(user):
    if not user:
        return ''
    return user.get_full_name() or user.username
