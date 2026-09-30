from django.http import Http404


def get_by_id_and_slug(queryset, pk, slug_field, slug):
    item = queryset.filter(pk=pk, **{slug_field: slug}).first()
    if item is None:
        item = queryset.filter(**{slug_field: slug}).order_by('pk').first()
    if item is None:
        raise Http404
    return item


def get_by_slug(queryset, slug_field, slug):
    item = queryset.filter(**{slug_field: slug}).order_by('pk').first()
    if item is None:
        raise Http404
    return item
