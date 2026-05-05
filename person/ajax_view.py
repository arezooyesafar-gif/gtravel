from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *

def ajax_user_list(request):
    users = User.objects.all()
    username = request.GET.get('user')
    if username:
        users = User.objects.filter(username=username)
    user_stat = request.GET.get('user_stat', None)
    if user_stat == '1':
        users = User.objects.filter(is_active=True)
    if user_stat == '0':
        users = User.objects.filter(is_active=False)
    paginator = Paginator(users,10)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    context = {
        'users': users
    }
    return render(request, 'ajax/ajax_user_list.html', context)