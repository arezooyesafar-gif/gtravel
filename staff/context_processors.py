from .access import user_menu


def staff_menu(request):
    return {
        'can': user_menu(getattr(request, 'user', None)),
        'staff_readonly': getattr(request, 'staff_readonly', False),
    }
