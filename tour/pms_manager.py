from django.contrib.auth.decorators import user_passes_test

def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)