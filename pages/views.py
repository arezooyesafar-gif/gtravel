from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from theme.models import index_page
from tour.dataset import get_top_pages, get_origin_menu_cities, get_menu_cities
from .dataset import get_colm_two_pages, get_colm_tree_pages
from .forms import *
from django.contrib.auth.decorators import user_passes_test
from .models import *
import os
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file = UploadedFile.objects.get(id=uploaded_file.id)
            file.delete()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'pages/upload_file.html', {'form': form})

def ads_upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file = UploadedFile.objects.get(id=uploaded_file.id)
            file.delete()
            return redirect('ads_file_list')
    else:
        form = FileUploadForm()
    return render(request, 'pages/upload_file.html', {'form': form})

def ajax_file_list(request):
    media_root = settings.MEDIA_ROOT
    files = []
    for root, dirs, file_names in os.walk(media_root):
        for file_name in file_names:
            files.append(os.path.relpath(os.path.join(root, file_name), media_root))
    paginator = Paginator(files,20)
    pagenumber = request.GET.get('page')
    files = paginator.get_page(pagenumber)
    context = {'files': files, 'media_url': settings.MEDIA_URL}
    return render(request, 'pages/ajax_file_list.html', context)

def ajax_ads_files(request):
    ads_media_root = os.path.join(settings.MEDIA_ROOT, 'ads')
    files = []
    for root, _, file_names in os.walk(ads_media_root):
        for file_name in file_names:
            files.append(os.path.relpath(os.path.join(root, file_name), ads_media_root))
    paginator = Paginator(files, 20)
    pagenumber = request.GET.get('page')
    files = paginator.get_page(pagenumber)
    context = {'files': files, 'ads_media_root':ads_media_root }
    return render(request, 'pages/ajax_ads_file_list.html', context)

def file_list(request):
    media_root = settings.MEDIA_ROOT
    if request.method == 'POST':
        file_to_delete = request.POST.get('file_to_delete')
        if file_to_delete:
            file_path = os.path.join(media_root, file_to_delete)
            try:
                os.remove(file_path)
                return redirect('file_list')
            except Exception as e:
                print(f"Error deleting file: {e}")
    return render(request, 'pages/file_list.html')

def ads_file_list(request):
    ads_media_root = os.path.join(settings.MEDIA_ROOT, 'ads')
    files = []
    for root, _, file_names in os.walk(ads_media_root):
        for file_name in file_names:
            files.append(os.path.relpath(os.path.join(root, file_name), ads_media_root))
    if request.method == 'POST':
        file_to_delete = request.POST.get('file_to_delete')
        if file_to_delete:
            file_path = os.path.join(ads_media_root, file_to_delete)
            try:
                os.remove(file_path)
                return redirect('ads_file_list')
            except Exception as e:
                print(f"Error deleting file: {e}")
    paginator = Paginator(files,20)
    pagenumber = request.GET.get('page')
    files = paginator.get_page(pagenumber)
    context = {'files': files,}
    return render(request, 'pages/file_list.html', context)

def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)

@superuser_required(login_url='login')
def create_page(request):
    forms = PageForm()
    if request.method == 'POST':
        forms = PageForm(request.POST, request.FILES)
        if forms.is_valid():
            forms = forms.save(commit=False)
            forms.save()
            return redirect('page_list')
    context = {
        'forms': forms
    }
    return render(request, 'pages/create_page.html', context)

def page_update(request, id):
    page = pages.objects.get(id=id)
    form = PageForm(instance=page)
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('page_list')
    context = {
        'forms': form,
        'page': page
    }
    return render(request, 'pages/create_page.html', context)

@superuser_required(login_url='login')
def page_list(request):
    all_pages = pages.objects.all()
    context = {
        'all_pages': all_pages
    }
    return render(request, 'pages/page_list.html', context)

def page_detail(request, slug):
    reseller_menu = get_top_pages()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    orgin_menu_cities = get_origin_menu_cities(69)
    cities_menu = get_menu_cities()
    theme_setting = index_page.objects.get(id=1)
    page = pages.objects.get(slug=slug)
    context = {
        'reseller_menu': reseller_menu,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'origins': orgin_menu_cities,
        'set': theme_setting,
        'page':page,
    }
    return render(request, 'ui/page.html', context)

def page_delete(request, id):
    page = pages.objects.get(id=id)
    page.delete()
    return redirect('page_list')