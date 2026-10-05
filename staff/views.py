from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StaffUserForm
from .models import ACTIONS, AREAS, REDIRECT_STATUSES, ChangeLog, RedirectRule, StaffAccess

superuser_only = user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')


@superuser_only
def staff_list(request):
    users = User.objects.filter(staff_access__isnull=False).select_related('staff_access').order_by('-id')
    search = request.GET.get('search', '').strip()
    if search:
        users = users.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
    paginator = Paginator(users, 25)
    context = {
        'users': paginator.get_page(request.GET.get('page')),
        'search': search,
    }
    return render(request, 'staff/staff-list.html', context)


@superuser_only
def staff_create(request):
    form = StaffUserForm()
    if request.method == 'POST':
        form = StaffUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'کاربر پشتیبانی ساخته شد')
            return redirect('staff-update', user.id)
        messages.error(request, 'اطلاعات وارد شده کامل نیست')
    return render(request, 'staff/staff-form.html', {'form': form})


@superuser_only
def staff_update(request, id):
    user = get_object_or_404(User, id=id)
    access, _ = StaffAccess.objects.get_or_create(user=user)
    form = StaffUserForm(instance=user, access=access)
    if request.method == 'POST':
        form = StaffUserForm(request.POST, instance=user, access=access)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسترسی های کاربر ذخیره شد')
            return redirect('staff-update', user.id)
        messages.error(request, 'اطلاعات وارد شده کامل نیست')
    context = {
        'form': form,
        'staff_user': user,
        'access': access,
    }
    return render(request, 'staff/staff-form.html', context)


@superuser_only
def staff_delete(request, id):
    user = get_object_or_404(User, id=id, is_superuser=False)
    user.delete()
    messages.success(request, 'کاربر پشتیبانی حذف شد')
    return redirect('staff-list')


def filtered_logs(params):
    logs = ChangeLog.objects.select_related('user')
    if params.get('user'):
        logs = logs.filter(user_id=params.get('user'))
    if params.get('action'):
        logs = logs.filter(action=params.get('action'))
    if params.get('area'):
        logs = logs.filter(area=params.get('area'))
    if params.get('from'):
        logs = logs.filter(created_at__date__gte=params.get('from'))
    if params.get('to'):
        logs = logs.filter(created_at__date__lte=params.get('to'))
    if params.get('search', '').strip():
        logs = logs.filter(title__icontains=params.get('search').strip())
    return logs


@superuser_only
def change_log(request):
    logs = filtered_logs(request.GET)
    selected_user = request.GET.get('user', '')
    selected_action = request.GET.get('action', '')
    selected_area = request.GET.get('area', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')
    search = request.GET.get('search', '').strip()
    paginator = Paginator(logs, 40)
    context = {
        'logs': paginator.get_page(request.GET.get('page')),
        'users': User.objects.filter(Q(staff_access__isnull=False) | Q(is_superuser=True)).order_by('username'),
        'areas': AREAS,
        'actions': ACTIONS,
        'selected_user': selected_user,
        'selected_action': selected_action,
        'selected_area': selected_area,
        'date_from': date_from,
        'date_to': date_to,
        'search': search,
    }
    return render(request, 'staff/change-log.html', context)


@superuser_only
def redirect_list(request):
    if request.method == 'POST':
        old_path = (request.POST.get('old_path') or '').strip()
        new_path = (request.POST.get('new_path') or '').strip()
        try:
            status = int(request.POST.get('status') or 301)
        except ValueError:
            status = 301
        if status not in (301, 302, 410):
            status = 301
        if not old_path:
            messages.error(request, 'آدرس قدیمی را وارد کنید')
        elif status != 410 and not new_path:
            messages.error(request, 'برای انتقال ۳۰۱ یا ۳۰۲ باید آدرس جدید را وارد کنید')
        else:
            if not old_path.startswith('/'):
                old_path = '/' + old_path
            RedirectRule.objects.update_or_create(
                old_path=old_path, defaults={'new_path': new_path, 'status': status})
            messages.success(request, 'ریدایرکت ذخیره شد')
        return redirect('redirect-list')
    items = RedirectRule.objects.all()
    search = request.GET.get('search', '').strip()
    if search:
        term = search
        if '://' in term:
            term = urlparse(term).path or term
        items = items.filter(Q(old_path__icontains=term) | Q(new_path__icontains=term))
    paginator = Paginator(items, 50)
    return render(request, 'staff/redirects.html', {
        'items': paginator.get_page(request.GET.get('page')),
        'statuses': REDIRECT_STATUSES,
        'search': search,
    })


@superuser_only
def redirect_delete(request, id):
    get_object_or_404(RedirectRule, id=id).delete()
    messages.success(request, 'ریدایرکت حذف شد')
    return redirect('redirect-list')


@superuser_only
def change_log_delete(request):
    if request.method != 'POST':
        return redirect('staff-change-log')
    mode = request.POST.get('mode')
    if mode == 'filtered':
        logs = filtered_logs(request.POST)
    else:
        ids = [value for value in request.POST.getlist('ids') if value.isdigit()]
        logs = ChangeLog.objects.filter(id__in=ids)
    count = logs.count()
    logs.delete()
    if count:
        messages.success(request, '%s ردیف از تاریخچه حذف شد' % count)
    else:
        messages.warning(request, 'ردیفی برای حذف انتخاب نشده بود')
    query = request.POST.get('query', '')
    url = redirect('staff-change-log').url
    return redirect('%s?%s' % (url, query) if query else url)
