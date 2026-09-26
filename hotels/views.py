from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from tour.dataset import get_all_hotels
from tour.models import City
from .forms import CreateHotelForm, hotel_search_form, CreateHotelMenuForm, hotel_comment_form
from .models import *
from tour.pms_manager import *


@superuser_required(login_url='login')
def ajax_hotel_list(request):
    hotellist = get_all_hotels().order_by('id')
    if 'hotel_name' in request.GET:
        hotel_name = request.GET['hotel_name']
        if hotel_name:
            hotellist = hotellist.filter(HotelName__contains=hotel_name).order_by('id')
    if 'hotel_name_eng' in request.GET:
        hotel_name_eng = request.GET['hotel_name_eng']
        if hotel_name_eng:
            hotellist = hotellist.filter(HotelNameEnglish__contains=hotel_name_eng).order_by('id')
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            city = City.objects.get(id=city)
            hotellist = hotellist.filter(Hcity=city).order_by('id')
    paginator = Paginator(hotellist, 20)
    page_number = request.GET.get('page')
    hotellist = paginator.get_page(page_number)
    context = {
        'Hotels': hotellist,
    }
    return render(request, 'hotel/ajax-hotels-list.html', context)


@superuser_required(login_url='login')
def ajax_hotel_cities(request):
    cities = Hotel_Data.objects.values_list('Hcity', flat=True).distinct()
    cities_data = []
    for i in cities:
        cities_data.append(City.objects.get(id=i))
    context = {
        'cities': cities_data
    }
    return render(request, 'hotel/hotel_cities.html', context)


# Hotel Menu CRUD
@superuser_required(login_url='login')
def CreateHotelMenu(request):
    forms = CreateHotelMenuForm()
    if request.method == 'POST':
        forms = CreateHotelMenuForm(request.POST)
        if forms.is_valid():
            forms.save()
            menus = Hotel_Menu.objects.all()
            context = {
                'form': forms,
                'Data': menus
            }
            return render(request, 'hotel/create-hotel-menu.html', context)
        else:
            menus = Hotel_Menu.objects.all()
            message = messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            context = {
                'form': forms,
                'message': message,
                'Data': menus
            }
            return render(request, 'hotel/create-hotel-menu.html', context)
    menus = Hotel_Menu.objects.all()
    context = {
        'form': forms,
        'Data': menus
    }
    return render(request, 'hotel/create-hotel-menu.html', context)


@superuser_required(login_url='login')
def UpdateHotelMenu(request, id):
    menu = Hotel_Menu.objects.get(id=id)
    forms = CreateHotelMenuForm(instance=menu)
    if request.method == 'POST':
        forms = CreateHotelMenuForm(request.POST, instance=menu)
        if forms.is_valid():
            forms.save()
            menus = Hotel_Menu.objects.all()
            return redirect('create-hotel-menu')
        else:
            menus = Hotel_Menu.objects.all()
            message = messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            context = {
                'form': forms,
                'message': message,
                'Data': menus
            }
            return render(request, 'hotel/create-hotel-menu.html', context)
    menus = Hotel_Menu.objects.all()
    context = {
        'form': forms,
        'Data': menus
    }
    return render(request, 'hotel/create-hotel-menu.html', context)

@superuser_required(login_url='login')
def DeleteHotelMenu(request, id):
    menu = Hotel_Menu.objects.get(id=id)
    menu.delete()
    return redirect('create-hotel-menu')

# Hotel CRUD Functions

@superuser_required(login_url='login')
def create_hotel(request):
    forms = CreateHotelForm()
    user = request.user
    if request.method == 'POST':
        forms = CreateHotelForm(request.POST, request.FILES)
        if forms.is_valid():
            hotel = forms.save(commit=False)
            hotel.Creator = user
            hotel.save()
            files = request.FILES.getlist('files')
            for file in files:
                hotel_file_instance = hotel_images(hotel=hotel, image=file)
                hotel_file_instance.save()
                messages.success(request, 'اطلاعات با موفقیت ذخیره گردید!')
                return redirect('create_hotel')
            messages.success(request, 'اطلاعات با موفقیت ذخیره گردید!')
            return redirect('create_hotel')
        else:
            messages.error(request, 'فیلدهای الزامی را جهت ورود اطلاعات هتل کامل نمایید')
            return redirect('create_hotel')
    context = {
        'form': forms
    }
    return render(request, 'hotel/create-hotel.html', context)


@superuser_required(login_url='login')
def update_hotel(request, id):
    hotel = Hotel_Data.objects.get(id=id)
    forms = CreateHotelForm(instance=hotel)
    galley = hotel_images.objects.filter(hotel=hotel)
    user = request.user
    if request.method == 'POST':
        forms = CreateHotelForm(request.POST, request.FILES, instance=hotel)
        if forms.is_valid():
            hotel_data = forms.save(commit=False)
            hotel_data.Creator = user
            hotel_data.save()
            files = request.FILES.getlist('files')
            for file in files:
                hotel_file_instance = hotel_images(hotel=hotel, image=file)
                hotel_file_instance.save()
            
            messages.success(request, 'اطلاعات با موفقیت ذخیره گردید!')
            return redirect('update_hotel', hotel.id)
        else:
            messages.error(request, 'فیلدهای الزامی را جهت ورود اطلاعات هتل کامل نمایید')
            return redirect('update_hotel', hotel.id)
    context = {
        'form': forms,
        'Data': hotel,
        'galley': galley
    }
    return render(request, 'hotel/create-hotel.html', context)


@superuser_required(login_url='login')
def delete_hotel(request, id):
    hotel = Hotel_Data.objects.get(id=id)
    hotel.delete()
    return redirect('hotel_list')


@superuser_required(login_url='login')
def hotel_list(request):
    forms = hotel_search_form()
    context = {
        'forms': forms
    }
    return render(request, 'hotel/hotels-list.html', context)

@superuser_required(login_url='login')
def remove_gallery_item(request, id):
    item = hotel_images.objects.get(id=id)
    hotel = item.hotel
    item.delete()
    return redirect('update_hotel', hotel.id)

@superuser_required(login_url='login')
def remove_hotel_image(request, id):
    hotel = Hotel_Data.objects.get(id=id)
    hotel.HotelImage = ''
    hotel.save()
    return redirect('update_hotel', hotel.id)

@superuser_required(login_url='login')
def comment_list(request):
    all_cms = hotel_comments.objects.all().order_by('-id')
    request.session['seen_hotel_comment_id'] = (
        hotel_comments.objects.order_by('-id').values_list('id', flat=True).first() or 0
    )
    paginator = Paginator(all_cms, 10)
    pagenumber = request.GET.get('page')
    all_cms = paginator.get_page(pagenumber)
    context = {
        'all_comments': all_cms
    }
    return render(request, 'hotel/comment-list.html', context)

@superuser_required(login_url='login')
def comment_update(request,id):
    item = hotel_comments.objects.get(id=id)
    forms = hotel_comment_form(instance=item)
    if request.method == 'POST':
        if request.POST.get('publish') == '1':
            item.publish = True
            item.save()
        if request.POST.get('publish') == '0':
            item.publish = False
            item.save()
        return redirect('comment_list')
    context = {
        'comment': item,
        'form': forms
    }
    return render(request, 'hotel/update-comment.html', context)

@superuser_required(login_url='login')
def comment_delete(request,id):
    item = hotel_comments.objects.filter(id=id)
    item.delete()
    return redirect('comment_list')