from .models import ACTIONS, AREAS, AREA_LABELS

MODULE_AREAS = {
    'hotels.views': 'hotels',
    'blog.views': 'blog',
    'pages.views': 'pages',
    'order.views': 'orders',
    'wallet.views': 'orders',
    'theme.views': 'settings',
    'tour.views.views_flights': 'flights',
    'tour.views.views_destination': 'destinations',
    'tour.views.views_packages': 'packages',
    'tour.views.views_tour': 'tours',
    'tour.pms_manager': 'settings',
    'staff.views': 'staff',
    'staff.message_views': 'messages',
}

NAME_AREAS = [
    ('reviews', ('tour-review', 'tour_review', 'tour-interest', 'tour_interest')),
    ('visas', ('visa',)),
    ('packages', ('package',)),
    ('hotels', ('hotel',)),
    ('flights', ('airline', 'airport')),
    ('blog', ('post', 'comment')),
    ('memories', ('memo', 'memory', 'memories')),
    ('pages', ('page', 'file', 'upload')),
    ('orders', ('order', 'reserv', 'wallet')),
    ('messages', ('message', 'msg', 'contact', 'subscribe', 'sub-delete', 'export-numbers')),
    ('users', ('user',)),
    ('destinations', ('country', 'city', 'spacial', 'media')),
    ('settings', ('about', 'slideshow', 'footer', 'faq', 'currency', 'dollar', 'api-partner', 'setting', 'theme', 'index')),
    ('tours', ('tour', 'trip_plan', 'date_plan', 'package')),
]

ADD_WORDS = ('create', 'add', 'register', 'upload', 'import', 'copy', 'start')
EDIT_WORDS = ('update', 'edit', 'change', 'toggle', 'publish', 'reset', 'reply', 'fetch')
DELETE_WORDS = ('delete', 'delet', 'remove')

IMPLIED_VIEW = {
    'packages': ('tours',),
}

FREE_NAMES = {'dashboard', 'login', 'logout', 'profile_view', 'index-page'}

SELF_NAMES = {'user_profile', 'user_profile_update'}


def resolve_action(url_name):
    name = (url_name or '').lower().replace('-', '_')
    for word in DELETE_WORDS:
        if word in name:
            return 'delete'
    for word in ADD_WORDS:
        if word in name:
            return 'add'
    for word in EDIT_WORDS:
        if word in name:
            return 'edit'
    return 'view'


def resolve_area(module, url_name):
    name = (url_name or '').lower()
    if module in MODULE_AREAS:
        return MODULE_AREAS[module]
    for area, words in NAME_AREAS:
        for word in words:
            if word in name:
                return area
    return ''


def get_access(user):
    if not user or not user.is_authenticated:
        return None
    return getattr(user, 'staff_access', None)


def user_can(user, area, action):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    access = get_access(user)
    if access is None or not area:
        return False
    if access.has(area, action):
        return True
    if action == 'view':
        if access.area_actions(area):
            return True
        return any(access.area_actions(other) for other in IMPLIED_VIEW.get(area, ()))
    return False


def user_menu(user):
    flags = {}
    for area, _ in AREAS:
        flags[area] = {action: user_can(user, area, action) for action, _ in ACTIONS}
        flags[area]['any'] = any(flags[area].values())
    flags['staff'] = {'any': bool(user and user.is_authenticated and user.is_superuser)}
    return flags


def area_label(area):
    return AREA_LABELS.get(area, area)
