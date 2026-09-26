from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from .access import resolve_area
from .current_user import get_current_user
from .models import ChangeLog, ObjectStamp

TRACKED_APPS = {'tour', 'hotels', 'blog', 'pages', 'order', 'theme', 'visa', 'wallet'}
SKIP_MODELS = {'staff.changelog', 'staff.staffaccess', 'staff.objectstamp', 'tour.viewcounter'}
SKIP_FIELDS = {'viewCount', 'view_count', 'updateDate', 'toursView', 'last_login'}
PARENT_MODELS = {'tour.tour', 'hotels.hotel_data', 'blog.blogposts'}

APP_AREAS = {
    'hotels': 'hotels',
    'blog': 'blog',
    'pages': 'pages',
    'order': 'orders',
    'wallet': 'orders',
    'theme': 'settings',
    'visa': 'visas',
}

MODEL_AREAS = {
    'tour.package': 'packages',
    'tour.mainpackage': 'packages',
    'tour.country': 'destinations',
    'tour.city': 'destinations',
    'tour.spacial_destinations': 'destinations',
    'tour.airline': 'flights',
    'tour.airport': 'flights',
    'tour.memories': 'memories',
    'tour.memo_category': 'memories',
    'tour.tourreview': 'reviews',
    'tour.contactus': 'messages',
    'tour.subscribe': 'messages',
}


def _label(instance):
    return '%s.%s' % (instance._meta.app_label, instance._meta.model_name)


def _area(instance):
    label = _label(instance)
    if label in MODEL_AREAS:
        return MODEL_AREAS[label]
    app = instance._meta.app_label
    if app in APP_AREAS:
        return APP_AREAS[app]
    return resolve_area('', instance._meta.model_name)


def _should_track(instance):
    if _label(instance) in SKIP_MODELS:
        return False
    return instance._meta.app_label in TRACKED_APPS


def _current_user():
    user = get_current_user()
    if user is None or not getattr(user, 'is_authenticated', False):
        return None
    return user


def _parents(instance):
    found = []
    for field in instance._meta.fields:
        related = getattr(field, 'related_model', None)
        if related is None or not field.many_to_one:
            continue
        label = '%s.%s' % (related._meta.app_label, related._meta.model_name)
        value = getattr(instance, field.attname, None)
        if label in PARENT_MODELS and value:
            found.append((label, str(value)))
    return found


def _stamp(user, label, object_id):
    ObjectStamp.objects.update_or_create(
        model_label=label,
        object_id=object_id,
        defaults={
            'updated_by': user,
            'updated_name': user.get_full_name() or user.username,
            'updated_at': timezone.now(),
        },
    )


def _write(user, instance, action):
    try:
        title = str(instance)
    except Exception:
        title = ''
    ChangeLog.objects.create(
        user=user,
        username=user.get_full_name() or user.username,
        action=action,
        area=_area(instance),
        model_label=_label(instance),
        model_title=instance._meta.verbose_name or instance._meta.model_name,
        object_id=str(getattr(instance, 'pk', '') or ''),
        title=title[:300],
    )


@receiver(post_save)
def log_save(sender, instance, created, update_fields=None, **kwargs):
    if not _should_track(instance):
        return
    if update_fields and set(update_fields) <= SKIP_FIELDS:
        return
    user = _current_user()
    if user is None:
        return
    _write(user, instance, 'add' if created else 'edit')
    label = _label(instance)
    if label in PARENT_MODELS and instance.pk:
        _stamp(user, label, str(instance.pk))
    for parent_label, parent_id in _parents(instance):
        _stamp(user, parent_label, parent_id)


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if not _should_track(instance):
        return
    user = _current_user()
    if user is None:
        return
    _write(user, instance, 'delete')
    for parent_label, parent_id in _parents(instance):
        _stamp(user, parent_label, parent_id)
