from urllib.parse import unquote, urlsplit

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseGone, HttpResponsePermanentRedirect, HttpResponseRedirect

from .models import RedirectRule

PROTECTED_PREFIXES = ('/dashboard/', '/admin/', '/static/', '/media/', '/user/', '/captcha/', '/ckeditor/')


def site_hosts(host=''):
    hosts = {value.lower().lstrip('.').split(':')[0] for value in list(settings.ALLOWED_HOSTS) + [host] if value and value != '*'}
    return hosts | {'www.' + value for value in hosts} | {value[4:] for value in hosts if value.startswith('www.')}


def split_url(value, host=''):
    if value.startswith('//'):
        value = 'http:' + value
    elif '://' not in value and not value.startswith('/'):
        first = value.split('/', 1)[0].split('?', 1)[0].split('#', 1)[0].split(':', 1)[0].lower()
        value = ('http://' if first in site_hosts(host) else '/') + value
    try:
        return urlsplit(value)
    except ValueError:
        return urlsplit('/' + value.lstrip('/'))


def clean_path(value, host=''):
    value = (value or '').strip()
    if not value:
        return ''
    return unquote(split_url(value, host).path) or '/'


def clean_target(value, host=''):
    value = (value or '').strip()
    if not value:
        return ''
    parts = split_url(value, host)
    if parts.scheme and parts.scheme.lower() not in ('http', 'https'):
        return ''
    if parts.netloc and (parts.hostname or '') not in site_hosts(host):
        return value
    target = unquote(parts.path) or '/'
    if parts.query:
        target += '?' + parts.query
    if parts.fragment:
        target += '#' + parts.fragment
    return target


def path_key(path):
    return path.split('#', 1)[0].split('?', 1)[0].rstrip('/') or '/'


def is_protected(path):
    return any(path == prefix.rstrip('/') or path.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def find_rule(path):
    candidates = [path]
    if path != '/':
        candidates.append(path[:-1] if path.endswith('/') else path + '/')
    rules = sorted(RedirectRule.objects.filter(old_path__in=candidates), key=lambda rule: rule.old_path != path)
    return rules[0] if rules else None


def creates_loop(old_path, target):
    seen = {path_key(old_path)}
    for _ in range(20):
        if '://' in target:
            return False
        key = path_key(target)
        if key in seen:
            return True
        seen.add(key)
        rule = find_rule(target.split('#', 1)[0].split('?', 1)[0])
        if rule is None or rule.status == 410 or not rule.new_path:
            return False
        target = rule.new_path
    return True


def search_filter(term, host=''):
    term = term.strip()
    path = clean_path(term, host)
    variants = {term, unquote(term)}
    if path != '/':
        variants |= {path, path.rstrip('/')}
    query = Q(old_path='/') | Q(new_path='/') if path == '/' else Q()
    for value in variants:
        if value:
            query |= Q(old_path__icontains=value) | Q(new_path__icontains=value)
    return query


def rule_response(rule, request):
    if rule.status == 410 or not rule.new_path:
        return HttpResponseGone()
    target = rule.new_path
    if '://' not in target and path_key(target) == path_key(request.path):
        return None
    query = request.META.get('QUERY_STRING', '')
    if query and '?' not in target:
        base, mark, fragment = target.partition('#')
        target = '%s?%s%s%s' % (base, query, mark, fragment)
    if rule.status == 302:
        return HttpResponseRedirect(target)
    return HttpResponsePermanentRedirect(target)
