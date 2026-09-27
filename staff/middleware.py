from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .access import FREE_NAMES, SELF_NAMES, resolve_action, resolve_area, user_can
from .current_user import set_current_user

ADMIN_NAMES = {
    'user_list', 'delete_user', 'ajax_user_list',
    'create_page', 'page_update', 'page_delete', 'page_list', 'file_list', 'ads_file_list',
    'upload_file', 'ads_upload_file', 'ajax_file_list', 'ajax_ads_files',
    'visa_list_admin', 'visa_view', 'visa_pdf', 'delete_visa_request',
    'delete_thai_visa_request',
    'main_page_settings', 'reset_password_admin',
}

WRITE_SQL = ('INSERT', 'UPDATE', 'DELETE', 'REPLACE', 'ALTER', 'DROP', 'CREATE', 'TRUNCATE')


class ReadOnlyBlocked(Exception):
    pass


class StaffAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(None)
        try:
            return self.get_response(request)
        finally:
            set_current_user(None)

    def process_view(self, request, view_func, view_args, view_kwargs):
        name = getattr(getattr(request, 'resolver_match', None), 'url_name', None)
        if not self._is_protected(request, name):
            return None
        user = getattr(request, 'user', None)
        set_current_user(user)
        if user is None or not user.is_authenticated:
            return redirect('login')
        if user.is_superuser or name in FREE_NAMES:
            return None
        if name in SELF_NAMES and str(view_kwargs.get('id', '')) == str(user.id):
            return None
        module = getattr(view_func, '__module__', '')
        area = resolve_area(module, name)
        action = resolve_action(name)
        if user_can(user, area, action):
            return None
        if not user_can(user, area, 'view'):
            return self._deny(request, area, action, view_only=False)
        if action == 'delete' or request.method not in ('GET', 'HEAD'):
            return self._deny(request, area, action, view_only=True)
        request.staff_readonly = True
        return self._run_read_only(request, view_func, view_args, view_kwargs, area, action)

    def _run_read_only(self, request, view_func, view_args, view_kwargs, area, action):
        attempts = []

        def block_writes(execute, sql, params, many, context):
            if sql.lstrip().upper().startswith(WRITE_SQL):
                attempts.append(sql)
                raise ReadOnlyBlocked()
            return execute(sql, params, many, context)

        try:
            with transaction.atomic():
                with connection.execute_wrapper(block_writes):
                    response = view_func(request, *view_args, **view_kwargs)
                    if hasattr(response, 'render') and not getattr(response, 'is_rendered', True):
                        response = response.render()
                if attempts:
                    raise ReadOnlyBlocked()
        except ReadOnlyBlocked:
            return self._deny(request, area, action, view_only=True)
        except Exception:
            if attempts:
                return self._deny(request, area, action, view_only=True)
            raise
        return response

    def _deny(self, request, area, action, view_only):
        message = 'شما فقط اجازه مشاهده این بخش را دارید و نمی توانید تغییری ثبت کنید.' if view_only else 'شما به این بخش دسترسی ندارید.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', ''):
            return JsonResponse({'error': message}, status=403)
        context = {
            'area': area,
            'action': action,
            'view_only': view_only,
            'message': message,
            'back_url': request.META.get('HTTP_REFERER', ''),
        }
        return render(request, 'staff/no-access.html', context, status=403)

    def _is_protected(self, request, name):
        if request.path.startswith('/dashboard/'):
            return True
        return name in ADMIN_NAMES or name in SELF_NAMES
