from django.contrib.auth.decorators import user_passes_test

def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser or hasattr(u, 'staff_access'), login_url=login_url)