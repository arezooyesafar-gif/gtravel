from django.http import HttpResponseGone, HttpResponsePermanentRedirect
from django.urls import Resolver404, resolve

SKIP_PREFIXES = ('/admin', '/dashboard', '/static', '/media')
NOINDEX_PREFIXES = ('/pdf-download/', '/user/', '/payment', '/save-tour-interest')
THICKBOX_PARAMS = ('TB_iframe', 'width', 'height')


def resolves(path):
    try:
        resolve(path)
    except Resolver404:
        return False
    return True


def clean_url(request):
    path = request.path
    params = request.GET.copy()
    changed = False
    bare = path.rstrip('/') or '/'
    if bare != path and not resolves(path) and resolves(bare):
        path = bare
        changed = True
    page = params.get('page')
    if page is not None and (not page.isdecimal() or int(page) < 2):
        params.pop('page')
        changed = True
    if 'TB_iframe' in params:
        for key in THICKBOX_PARAMS:
            params.pop(key, None)
        changed = True
    if not changed:
        return None
    query = params.urlencode()
    return path + ('?' + query if query else '')


class SeoRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('GET', 'HEAD') and not request.path.startswith(SKIP_PREFIXES):
            target = clean_url(request)
            if target is not None:
                return HttpResponsePermanentRedirect(target)
        response = self.get_response(request)
        path = request.path
        is_pdf = path.lower().endswith('.pdf')
        if response.status_code == 404 and is_pdf and path.startswith('/media/uploads/'):
            response = HttpResponseGone()
        if is_pdf or path.startswith(NOINDEX_PREFIXES):
            response['X-Robots-Tag'] = 'noindex, nofollow'
        return response
