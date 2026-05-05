from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *
from .forms import *

@login_required(login_url='login')
def main_page_settings(request, id):
    theme_setting = index_page.objects.get(id=1)
    forms = update_main_page(instance=theme_setting)
    if request.method == 'POST':
        forms = update_main_page(request.POST, request.FILES, instance=theme_setting)
        if forms.is_valid():
            forms.save()
            return redirect('main_page_settings', theme_setting.id)
    context = {
        'forms': forms
    }
    return render(request, 'theme/main_set.html', context)