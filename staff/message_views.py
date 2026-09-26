from django.contrib import messages as flash
from django.shortcuts import redirect
from tour.models import ContactUs

from .access import user_can
from .current_user import get_current_user, set_current_user
from .models import ChangeLog


def bulk_delete_messages(request):
    if request.method != 'POST':
        return redirect('messages')
    user = request.user
    if not user_can(user, 'messages', 'delete'):
        flash.warning(request, 'شما اجازه حذف پیام ها را ندارید')
        return redirect('messages')
    if request.POST.get('mode') == 'all':
        items = ContactUs.objects.all()
    else:
        ids = [value for value in request.POST.getlist('ids') if value.isdigit()]
        items = ContactUs.objects.filter(id__in=ids)
    count = items.count()
    if not count:
        flash.warning(request, 'پیامی برای حذف انتخاب نشده بود')
        return redirect('messages')
    keeper = get_current_user()
    set_current_user(None)
    items.delete()
    set_current_user(keeper)
    ChangeLog.objects.create(
        user=user,
        username=user.get_full_name() or user.username,
        action='delete',
        area='messages',
        model_label='tour.contactus',
        model_title='پیام تماس با ما',
        title='حذف گروهی %s پیام' % count,
    )
    flash.success(request, '%s پیام حذف شد' % count)
    return redirect('messages')
